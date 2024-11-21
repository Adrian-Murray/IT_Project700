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
        user = User.query.get(user_id)
        if not user:
            logger.error(f"User {user_id} not found")
            return None, 0
            
        profile = ReferenceProfile.query.get(user.reference_profile_id)
        if not profile:
            logger.warning(f"No profile found for user {user_id}")
            return None, 0
            
        # Read the career data
        df = pd.read_csv('data/career_recommendation_with_courses.csv')
        
        # Calculate skills match for each career
        user_skills = set(user.skills.split(", ")) if user.skills else set()
        
        # Calculate personality match
        personality_scores = []
        for _, row in df.iterrows():
            # Calculate personality distance
            personality_distance = math.sqrt(
                (row['Dominance'] - profile.dominance) ** 2 +
                (row['Extraversion'] - profile.extraversion) ** 2 +
                (row['Patience'] - profile.patience) ** 2 +
                (row['Formality'] - profile.formality) ** 2
            )
            
            # Calculate skills match
            career_skills = set(str(row['Key Skills']).split(",")) if pd.notna(row['Key Skills']) else set()
            skills_match = len(user_skills.intersection(career_skills)) / len(career_skills) if career_skills else 0
            
            # Combined score (weighted average)
            personality_weight = 0.7
            skills_weight = 0.3
            
            # Normalize personality distance to 0-1 scale (inverse it so higher is better)
            max_distance = math.sqrt(4 * 100)  # Maximum possible distance
            personality_score = 1 - (personality_distance / max_distance)
            
            # Calculate final score
            final_score = (personality_weight * personality_score) + (skills_weight * skills_match)
            
            personality_scores.append({
                'career': row['Recommended Career'],
                'score': final_score,
                'skills_match': skills_match,
                'personality_match': personality_score
            })
        
        # Get best match
        best_match = max(personality_scores, key=lambda x: x['score'])
        
        # Convert score to percentage
        match_percentage = round(best_match['score'] * 100, 2)
        
        logger.info(f"Career prediction for user {user_id}: {best_match['career']} ({match_percentage}%)")
        
        return best_match['career'], match_percentage
        
    except Exception as e:
        logger.error(f"Error in career recommendation: {str(e)}")
        return None, 0