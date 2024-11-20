import pandas as pd
import math
from sklearn import logger
from models import User, BehavioralAssessment, ReferenceProfile
import joblib
import logging
from ml.feature_engineering import create_derived_features, calculate_skill_match

# recommendation.py
def calculate_reference_profile(user_id):
    """Calculate the best matching reference profile for a user"""
    factors = {"Dominance": 0, "Extraversion": 0, "Patience": 0, "Formality": 0}
    assessments = BehavioralAssessment.query.filter_by(user_id=user_id).all()
    
    if not assessments:
        logger.warning(f"No assessments found for user {user_id}")
        return None

    # Calculate factor scores
    for assessment in assessments:
        if assessment.question_type == "Expected":
            factors[assessment.factor] += 1
        elif assessment.question_type == "Self-description":
            factors[assessment.factor] += 2
   
    # Get all reference profiles
    profiles = ReferenceProfile.query.all()
    if not profiles:
        logger.warning("No reference profiles found in database")
        return None

    # Find best matching profile
    best_profile = None
    lowest_distance = float('inf')

    for profile in profiles:
        if not all(hasattr(profile, attr) for attr in ['dominance', 'extraversion', 'patience', 'formality']):
            continue
            
        distance = math.sqrt(
            (factors["Dominance"] - profile.dominance) ** 2 +
            (factors["Extraversion"] - profile.extraversion) ** 2 +
            (factors["Patience"] - profile.patience) ** 2 +
            (factors["Formality"] - profile.formality) ** 2
        )
        
        if distance < lowest_distance:
            lowest_distance = distance
            best_profile = profile

    if best_profile:
        logger.info(f"Found matching profile {best_profile.name} for user {user_id}")
        return best_profile.id
    else:
        logger.warning(f"No suitable profile found for user {user_id}")
        return None

def career_recommendation(user_id):
    try:
        # Load model
        model = joblib.load("models/career_recommendation_model.pkl")
        
        # Get user data
        user = User.query.get(user_id)
        if not user:
            logger.error(f"User {user_id} not found")
            return None, 0
            
        # Get user's profile
        profile = ReferenceProfile.query.get(user.reference_profile_id)
        if not profile:
            logger.warning(f"No profile found for user {user_id}")
            return None, 0
            
        # Calculate skill match
        df = pd.read_csv('data/courses_cleaned.csv', delimiter=';')
        course_skills = df[df['Course'] == user.course]['Key Skills'].iloc[0] if len(df[df['Course'] == user.course]) > 0 else ''
        skill_match = calculate_skill_match(user.skills, course_skills)
        
        # Prepare features
        user_features = {
            "Course": user.course or "Undecided",
            "Universities_ID": user.university_id or "NONE",
            "Faculty/Department": user.faculty or "Undecided",
            "Duration": user.duration or 0,
            "Age": user.age,
            "Dominance": profile.dominance,
            "Extraversion": profile.extraversion,
            "Patience": profile.patience,
            "Formality": profile.formality,
            "skill_match_score": skill_match
        }
        
        # Create DataFrame and add derived features
        user_df = pd.DataFrame([user_features])
        user_df = create_derived_features(user_df)
        
        # Make prediction
        prediction = model.predict(user_df)[0]
        confidence = model.predict_proba(user_df).max() * 100
        
        logger.info(f"Career prediction for user {user_id}: {prediction} ({confidence:.2f}%)")
        
        return prediction, round(confidence, 2)
        
    except Exception as e:
        logger.error(f"Error in career recommendation: {str(e)}")
        return None, 0