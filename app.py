from flask import Config, Flask, jsonify, request, send_file, render_template_string
from flask_cors import CORS
import pandas as pd
from extensions import db, cors
import init_data
from models import User, BehavioralAssessment, ReferenceProfile, Course, University
from recommendation import career_recommendation, calculate_reference_profile
import io
import os
import bcrypt
import logging
import traceback
import jwt
from datetime import datetime, timedelta
from functools import wraps

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
cors.init_app(app, supports_credentials=True)

# Configuration
app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=True,
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'your-secret-key-here'),
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1)
)

# Initialize extensions
db.init_app(app)

import logging
from typing import List, Dict, Any

def get_career_progression(career: str) -> List[Dict[str, Any]]:
    """
    Generate career progression path for a given career.
    Args:
        career (str): The career title to generate progression for
    Returns:
        List[Dict]: A list of career stages with title, years of experience, and salary
    """
    # Career progression mapping with defined paths for different careers
    career_paths = {
        "Software Engineer": [
            {"title": "Junior Software Engineer", "years": 0, "salary": 45000},
            {"title": "Software Engineer", "years": 2, "salary": 75000},
            {"title": "Senior Software Engineer", "years": 5, "salary": 95000},
            {"title": "Lead Software Engineer", "years": 8, "salary": 120000}
        ],
        "Data Scientist": [
            {"title": "Junior Data Scientist", "years": 0, "salary": 48000},
            {"title": "Data Scientist", "years": 2, "salary": 78000},
            {"title": "Senior Data Scientist", "years": 5, "salary": 98000},
            {"title": "Lead Data Scientist", "years": 8, "salary": 125000}
        ],
        "Public Defender": [
            {"title": "Junior Public Defender", "years": 0, "salary": 42000},
            {"title": "Public Defender", "years": 3, "salary": 65000},
            {"title": "Senior Public Defender", "years": 6, "salary": 85000},
            {"title": "Chief Public Defender", "years": 9, "salary": 110000}
        ],
        "Accountant": [
            {"title": "Junior Accountant", "years": 0, "salary": 40000},
            {"title": "Staff Accountant", "years": 2, "salary": 60000},
            {"title": "Senior Accountant", "years": 5, "salary": 80000},
            {"title": "Finance Manager", "years": 8, "salary": 100000}
        ],
        "Operations Manager": [
            {"title": "Operations Coordinator", "years": 0, "salary": 45000},
            {"title": "Operations Manager", "years": 3, "salary": 70000},
            {"title": "Senior Operations Manager", "years": 6, "salary": 90000},
            {"title": "Director of Operations", "years": 9, "salary": 115000}
        ],
        "General Practitioner": [
            {"title": "Medical Resident", "years": 0, "salary": 52000},
            {"title": "General Practitioner", "years": 3, "salary": 120000},
            {"title": "Senior GP", "years": 6, "salary": 150000},
            {"title": "Medical Director", "years": 10, "salary": 180000}
        ],
        "Civil Engineer": [
            {"title": "Junior Civil Engineer", "years": 0, "salary": 48000},
            {"title": "Civil Engineer", "years": 3, "salary": 75000},
            {"title": "Senior Civil Engineer", "years": 6, "salary": 95000},
            {"title": "Project Director", "years": 9, "salary": 120000}
        ],
        "IT Support Specialist": [
            {"title": "IT Support Technician", "years": 0, "salary": 35000},
            {"title": "IT Support Specialist", "years": 2, "salary": 50000},
            {"title": "Senior IT Support Specialist", "years": 4, "salary": 65000},
            {"title": "IT Support Manager", "years": 7, "salary": 85000}
        ]
    }

    try:
        # If we have a defined path for this career, return it
        if career in career_paths:
            logger.info(f"Found defined career path for: {career}")
            return career_paths[career]

        # If no specific path is defined, generate a generic progression
        logger.info(f"Generating generic career path for: {career}")
        return [
            {"title": f"Junior {career}", "years": 0, "salary": 40000},
            {"title": career, "years": 2, "salary": 60000},
            {"title": f"Senior {career}", "years": 5, "salary": 80000},
            {"title": f"Lead {career}", "years": 8, "salary": 100000}
        ]

    except Exception as e:
        logger.error(f"Error generating career progression for {career}: {str(e)}")
        return []

if __name__ == "__main__":
    with app.app_context():
        try:
            # Initialize database tables
            db.create_all()

            # Load reference profiles
            if ReferenceProfile.query.count() == 0:
                init_data.init_reference_profiles(app)

            # Load universities
            if University.query.count() == 0:
                init_data.init_universities(app)

            # Load courses
            if Course.query.count() == 0:
                init_data.init_courses(app)

            logger.info("Application initialized successfully")
        except Exception as e:
            logger.error(f"Error during initialization: {str(e)}")

    # Start the app
    app.run(debug=True)


# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
            
        try:
            if token.startswith('Bearer '):
                token = token.split(" ")[1]
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'error': 'Invalid user'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

# Database initialization
def init_db():
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            logger.error(traceback.format_exc())

init_db()

# Authentication routes
@app.route('/signup', methods=['POST'])
def signup():
    try:
        logger.debug("Received signup request")
        data = request.json
        logger.debug(f"Signup data received: {data}")

        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'age', 'careerInterests', 'password']
        if not all(field in data for field in required_fields):
            logger.error("Missing required fields")
            return jsonify({"error": "Required fields are missing"}), 400

        # Check existing user
        if User.query.filter_by(email=data['email']).first():
            logger.error(f"User with email {data['email']} already exists")
            return jsonify({"error": "Email already in use"}), 400

        try:
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            
            new_user = User(
                first_name=data['firstName'],
                last_name=data['lastName'],
                email=data['email'],
                age=data['age'],
                skills=", ".join(data.get('skills', [])),
                career_interests=data['careerInterests'],
                password=hashed_password,
                course="Undecided",
                university_id="NONE",
                faculty="Undecided",
                duration=0
            )

            db.session.add(new_user)
            db.session.commit()
            
            # Generate token
            token = jwt.encode({
                'user_id': new_user.id,
                'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
            }, app.config['JWT_SECRET_KEY'])

            return jsonify({
                "message": "User signed up successfully",
                "user_id": new_user.id,
                "token": token,
                "user": {
                    "firstName": new_user.first_name,
                    "lastName": new_user.last_name,
                    "email": new_user.email,
                    "skills": data.get('skills', []),
                    "careerInterests": new_user.career_interests
                }
            })

        except Exception as e:
            db.session.rollback()
            logger.error(f"Database error during user creation: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({"error": f"Database error: {str(e)}"}), 500

    except Exception as e:
        logger.error(f"Unexpected error in signup: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
            }, app.config['JWT_SECRET_KEY'])
            
            return jsonify({
                "message": "Login successful",
                "user_id": user.id,
                "token": token,
                "user": {
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "email": user.email,
                    "skills": user.skills.split(", ") if user.skills else [],
                    "careerInterests": user.career_interests
                }
            })
        return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"error": "Login failed"}), 500

# Protected routes
@app.route('/user/profile', methods=['GET'])
@token_required
def get_user_profile(current_user):
    try:
        profile = ReferenceProfile.query.get(current_user.reference_profile_id)
        profile_data = {
            "id": profile.id,
            "name": profile.name,
            "description": profile.description,
            "dominance": profile.dominance,
            "extraversion": profile.extraversion,
            "patience": profile.patience,
            "formality": profile.formality
        } if profile else None
        
        return jsonify({
            "user": {
                "firstName": current_user.first_name,
                "lastName": current_user.last_name,
                "email": current_user.email,
                "age": current_user.age,
                "skills": current_user.skills.split(", ") if current_user.skills else [],
                "careerInterests": current_user.career_interests,
                "profile": profile_data
            }
        })
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        return jsonify({"error": "Failed to get user profile"}), 500

@app.route('/user/profile', methods=['PUT'])
@token_required
def update_user_profile(current_user):
    try:
        data = request.json
        
        # Update user fields if provided
        for field in ['firstName', 'lastName', 'age', 'careerInterests']:
            if field in data:
                setattr(current_user, field, data[field])
        
        if 'skills' in data:
            current_user.skills = ", ".join(data['skills'])
            
        db.session.commit()
        
        return jsonify({
            "message": "Profile updated successfully",
            "user": {
                "firstName": current_user.first_name,
                "lastName": current_user.last_name,
                "email": current_user.email,
                "age": current_user.age,
                "skills": current_user.skills.split(", ") if current_user.skills else [],
                "careerInterests": current_user.career_interests
            }
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f"Profile update error: {str(e)}")
        return jsonify({"error": "Failed to update profile"}), 500

@app.route('/submit_assessment', methods=['POST'])
@token_required
def submit_assessment(current_user):
    try:
        data = request.json
        responses = data.get('responses')

        if not responses:
            return jsonify({"error": "Responses are required"}), 400

        # Clear existing assessments
        BehavioralAssessment.query.filter_by(user_id=current_user.id).delete()

        for response in responses:
            adjective = response['adjective']
            question_type = response['question_type']
            factor = get_factor(adjective)
            assessment_entry = BehavioralAssessment(
                user_id=current_user.id,
                adjective=adjective,
                question_type=question_type,
                factor=factor
            )
            db.session.add(assessment_entry)

        db.session.commit()

        profile_id = calculate_reference_profile(current_user.id)
        current_user.reference_profile_id = profile_id
        db.session.commit()

        profile = ReferenceProfile.query.get(profile_id)
        
        return jsonify({
            "message": "Assessment submitted successfully",
            "profile": {
                "id": profile.id,
                "name": profile.name,
                "description": profile.description
            }
        })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Assessment submission error: {str(e)}")
        return jsonify({"error": "Failed to submit assessment"}), 500

@app.route('/recommend', methods=['GET'])
@token_required
def recommend(current_user):
    try:
        career, rating = career_recommendation(current_user.id)
        if career is None:
            return jsonify({"error": "Recommendation could not be generated"}), 500

        related_courses = Course.query.filter_by(recommended_career=career).all()
        courses_and_schools = [
            {
                "course": course.name,
                "school": University.query.get(course.university_id).name,
                "duration": course.duration,
                "keySkills": course.key_skills.split(", ") if course.key_skills else []
            }
            for course in related_courses
        ]

        return jsonify({
            "name": f"{current_user.first_name} {current_user.last_name}",
            "career_recommendation": career,
            "recommendation_rating": rating,
            "related_courses_and_schools": courses_and_schools
        })
    except Exception as e:
        logger.error(f"Recommendation error: {str(e)}")
        return jsonify({"error": "Failed to generate recommendation"}), 500

# Utility functions
def get_factor(adjective):
    # Convert adjective to lowercase and remove any whitespace
    adjective = adjective.lower().strip()
    
    factor_mapping = {
        # Dominance factors
        "assertive": "Dominance",
        "confident": "Dominance",
        "decisive": "Dominance",
        "ambitious": "Dominance",
        "bold": "Dominance",
        "commanding": "Dominance",
        "competitive": "Dominance",
        "determined": "Dominance",
        "independent": "Dominance",
        "fast-paced": "Dominance",
        "achievement": "Dominance",
        
        # Extraversion factors
        "sociable": "Extraversion",
        "outgoing": "Extraversion",
        "friendly": "Extraversion",
        "communicative": "Extraversion",
        "enthusiastic": "Extraversion",
        "persuasive": "Extraversion",
        "lively": "Extraversion",
        "talkative": "Extraversion",
        "engaging": "Extraversion",
        "energetic": "Extraversion",
        "teamwork": "Extraversion",
        
        # Patience factors
        "calm": "Patience",
        "steady": "Patience",
        "patient": "Patience",
        "consistent": "Patience",
        "reliable": "Patience",
        "composed": "Patience",
        "accommodating": "Patience",
        "predictable": "Patience",
        "supportive": "Patience",
        "stable": "Patience",
        "consistency": "Patience",
        
        # Formality factors
        "structured": "Formality",
        "precise": "Formality",
        "detail-oriented": "Formality",
        "methodical": "Formality",
        "organized": "Formality",
        "careful": "Formality",
        "disciplined": "Formality",
        "conscientious": "Formality",
        "rule-following": "Formality",
        "excellence": "Formality",
        "collaborative": "Formality"
    }
    
    factor = factor_mapping.get(adjective)
    if not factor:
        logger.warning(f"Unknown adjective encountered: {adjective}")
        return "Dominance"  # Default factor if unknown
    return factor

@app.route('/career_path', methods=['GET'])
@token_required
def get_career_path_route(current_user):
    try:
        # Check if user has completed assessment
        if not current_user.reference_profile_id:
            return jsonify({
                "error": "Please complete the assessment first",
                "redirect": "/assessment"
            }), 400
            
        # Get career recommendation
        career, rating = career_recommendation(current_user.id)
        if not career:
            logger.error(f"Unable to generate career recommendation for user {current_user.id}")
            return jsonify({
                "error": "Unable to generate career path",
                "redirect": "/assessment"
            }), 400
            
        # Get career progression data
        progression = get_career_progression(career)
        
        if not progression:
            logger.error(f"Unable to generate career progression for career: {career}")
            return jsonify({"error": "Failed to generate career progression"}), 500
        
        # Return both career recommendation and progression
        return jsonify({
            "current_career": career,
            "match_rating": rating,
            "progression": progression
        })
        
    except Exception as e:
        logger.error(f"Error in career path route: {str(e)}")
        return jsonify({"error": "Failed to load career data"}), 500

@app.route('/dashboard')
@token_required
def get_dashboard(current_user):
    if not current_user.reference_profile_id:
        return jsonify({"error": "Assessment required"}), 400

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

# CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == "__main__":
    app.run(debug=True)