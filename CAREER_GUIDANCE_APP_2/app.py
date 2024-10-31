from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base



import re
import datetime
import os







# Initialize the Flask application
app = Flask(__name__)
# Secret key for session management
app.secret_key = 'supersecretkey'

# Configure the SQLite database URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'resource/users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

# Initialize the database connection
db = SQLAlchemy(app)
Base = declarative_base()








class User(db.Model):
    __tablename__ = 'Users'  # Table name in the database
    user_id = db.Column(db.Integer, primary_key=True)  # Primary key
    email = db.Column(db.String(100), unique=True, nullable=False)  # User's email, must be unique
    password = db.Column(db.String(100), nullable=False)  # User's password (hashed)
    name = db.Column(db.String(100), nullable=False)  # User's first name
    surname = db.Column(db.String(100), nullable=False)  # User's last name
    mobile_number = db.Column(db.String(100), nullable=False)  # User's mobile number
    date_of_birth = db.Column(db.String(100), nullable=False)  # User's date of birth
    education_level = db.Column(db.String(100), nullable=False)  # User's education level
    
    # Define relationships
    skills = db.relationship('user_skills', back_populates='user')
    hobbies = db.relationship('user_hobbies', back_populates='user')


class user_hobbies(db.Model):
    __tablename__ = 'user_hobbies'

    hobby_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    main_hobby = db.Column(db.String(100), nullable=False)
    additional_hobby_1 = db.Column(db.String(100), nullable=True)
    additional_hobby_2 = db.Column(db.String(100), nullable=True)
    additional_hobby_3 = db.Column(db.String(100), nullable=True)

    # Relationship
    user = db.relationship('User', back_populates='hobbies')


class user_skills(db.Model):
    __tablename__ = 'user_skills'

    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    main_skill = db.Column(db.String(100), nullable=False)
    additional_skill_1 = db.Column(db.String(100), nullable=True)
    additional_skill_2 = db.Column(db.String(100), nullable=True)
    additional_skill_3 = db.Column(db.String(100), nullable=True)

    # Relationship
    user = db.relationship('User', back_populates='skills')

    

class PersonalityTestQuestions(db.Model):
    __tablename__ = 'PersonalityTestQuestions'  # Table name in the database
    question_id = db.Column(db.Integer, primary_key=True)  # Primary key for questions
    question_text = db.Column(db.String(255), nullable=False)  # Text of the question
    answers = db.relationship("PersonalityTestAnswers", back_populates="question")  # Relationship with answers


class PersonalityTestAnswers(db.Model):
    __tablename__ = 'PersonalityTestAnswers'  # Table name in the database
    answer_id = db.Column(db.Integer, primary_key=True)  # Primary key for answers
    answer_text = db.Column(db.String, nullable=False)  # Text of the answer
    question_id = db.Column(db.Integer, db.ForeignKey('PersonalityTestQuestions.question_id'))  # Foreign key to questions
    answer_value = db.Column(db.Integer)  # Numerical value associated with the answer
    category = db.Column(db.String)  # Category for the answer (e.g., Introverted, Extroverted)

    # Define a relationship to link back to questions
    question = db.relationship('PersonalityTestQuestions', back_populates='answers')


class Skills(db.Model):
    __tablename__ = 'skills'  # Define table name for Skills
    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), unique=True)


class Hobbies(db.Model):
    __tablename__ = 'hobbies'  # Define table name for Hobbies
    hobby_id = db.Column(db.Integer, primary_key=True)
    hobby_name = db.Column(db.String(100), unique=True)


# Define the model for storing Personality Test Scores
class PersonalityTestScores(db.Model):
    __tablename__ = 'PersonalityTestScores'  # Table name in the database
    score_id = db.Column(db.Integer, primary_key=True)  # Primary key for scores
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))  # Foreign key to Users
    # Columns to store scores for each personality category, initialized to 0
    E = db.Column(db.Integer, default=0)  # Extroversion score
    I = db.Column(db.Integer, default=0)  # Introversion score
    S = db.Column(db.Integer, default=0)  # Sensing score
    N = db.Column(db.Integer, default=0)  # Intuition score
    T = db.Column(db.Integer, default=0)  # Thinking score
    F = db.Column(db.Integer, default=0)  # Feeling score
    J = db.Column(db.Integer, default=0)  # Judging score
    P = db.Column(db.Integer, default=0)  # Perceiving score




# Define the model for user personality types
class user_personality_types(db.Model):
    __tablename__ = 'user_personality_types'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key for personality types
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)  # Foreign key to Users
    primary_personality_type = db.Column(db.String, nullable=False)  # Primary personality type of the user
    alternative_1 = db.Column(db.String)  # First alternative personality type
    alternative_2 = db.Column(db.String)  # Second alternative personality type
    alternative_3 = db.Column(db.String)  # Third alternative personality type







# Validation Helper Functions
def is_valid_email(email):
    """Validate the email format using a regular expression."""
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def is_valid_name(name):
    """Validate that the name contains only letters."""
    return re.match(r'^[A-Za-z]+$', name)

def is_valid_mobile_number(mobile_number):
    """Validate mobile number format based on its prefix."""
    if mobile_number.startswith('+'):
        return re.match(r'^\+[0-9]{10,15}$', mobile_number)  # International format
    else:
        return re.match(r'^[0-9]{10,15}$', mobile_number)  # Local format

def is_valid_date_of_birth(date_of_birth):
    """Check if the date of birth is valid and user is at least 10 years old."""
    try:
        birth_date = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')  # Parse date
        today = datetime.datetime.today()  # Current date
        age = (today - birth_date).days // 365  # Calculate age in years
        return birth_date < today and age >= 10  # Ensure valid age
    except ValueError:
        return False  # Invalid date format

def is_valid_education(education_level):
    """Check if the provided education level is valid."""
    valid_education_levels = ['Matric', 'University', 'Grade 10 or below']  # List of acceptable levels
    return education_level in valid_education_levels  # Return true if the level is valid






# Index route
@app.route('/')
def index():
    """Redirect to the home page."""
    return redirect(url_for('home'))  # Redirect the user to the 'home' route



# Sign-up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user sign-up."""
    if request.method == 'POST':  # Check if the form has been submitted
        # Retrieve form data
        email = request.form['email']  # Get the email from the form
        password = request.form['password']  # Get the password from the form
        name = request.form['name']  # Get the user's first name
        surname = request.form['surname']  # Get the user's last name
        mobile_number = request.form['mobile_number']  # Get the user's mobile number
        date_of_birth = request.form['date_of_birth']  # Get the user's date of birth
        education_level = request.form['education_level']  # Get the user's education level

        # Initialize a list to hold any validation errors
        errors = []

        # Perform validation checks for user input
        if not is_valid_email(email):
            errors.append('Invalid email format.')  # Check for valid email format
        
        if not is_valid_name(name) or not is_valid_name(surname):
            errors.append('Name and surname should not contain numbers or special characters.')  # Validate name and surname
        
        if not is_valid_mobile_number(mobile_number):
            errors.append('Invalid mobile number format.')  # Validate mobile number format
        
        if not is_valid_date_of_birth(date_of_birth):
            errors.append('Invalid date of birth. Ensure it\'s in YYYY-MM-DD format and you are above 10 years old.')  # Validate date of birth
        
        if not is_valid_education(education_level):
            errors.append('Please select a valid education level.')  # Validate education level

        # Check if the user already exists in the database
        user = User.query.filter_by(email=email).first()  # Query to find existing user by email
        if user:
            errors.append('User already exists. Please log in.')  # Append error if user already exists

        # If there are any validation errors, render the sign-up template with error messages
        if errors:
            for error in errors:
                flash(error)  # Flash each error message to the user
            return render_template('signup.html', email=email, name=name, surname=surname,
                                   mobile_number=mobile_number, date_of_birth=date_of_birth,
                                   education_level=education_level)  # Re-render the sign-up form with existing data

        # Hash the password for security before storing it in the database
        hashed_password = generate_password_hash(password)

        # Create a new User object and populate it with the form data
        new_user = User(email=email, password=hashed_password, name=name, surname=surname,
                        mobile_number=mobile_number, date_of_birth=date_of_birth, education_level=education_level)

        # Add the new user to the session and commit it to the database
        db.session.add(new_user)  # Add new user to the session
        db.session.commit()  # Commit the session to the database

        flash('Sign up successful! Please proceed to select your hobbies and skills.')  # Notify the user of a successful sign-up
        return redirect(url_for('select_hobbies_skills'))  # Redirect the user to the hobbies and skills page

    return render_template('signup.html')  # If GET request, render the sign-up template



@app.route('/select_hobbies_skills', methods=['GET', 'POST'])
def select_hobbies_skills():
    """Handle hobbies and skills selection after sign-up."""
    if request.method == 'POST':
        # Get user_id from session
        user_id = session.get('user_id')  
        if not user_id:
            flash('User not found. Please sign up first.')
            return redirect(url_for('signup'))  

        # Get selected hobbies and skills from the form
        selected_hobbies = request.form.getlist('main_hobby') + request.form.getlist('additional_hobbies')
        selected_skills = request.form.getlist('main_skill') + request.form.getlist('additional_skills')

        # Debugging: Print selected hobbies and skills
        print("Selected Hobbies:", selected_hobbies)
        print("Selected Skills:", selected_skills)

        # Validate the number of selected hobbies
        if len(selected_hobbies) > 4:
            flash('Please select no more than 4 hobbies.')
            return redirect(url_for('select_hobbies_skills'))

        # Validate the number of selected skills
        if len(selected_skills) > 4:
            flash('Please select no more than 4 skills.')
            return redirect(url_for('select_hobbies_skills'))

        # Call function to insert hobbies and skills into the database
        insert_hobbies_and_skills(user_id, selected_hobbies, selected_skills)

        flash('Hobbies and skills selected successfully!')  
        return redirect(url_for('login'))  

    # Fetch predefined hobbies and skills from the database
    hobbies = Hobbies.query.all()
    skills = Skills.query.all()
    
    return render_template('select_hobbies_skills.html', hobbies=hobbies, skills=skills)

def insert_hobbies_and_skills(user_id, selected_hobbies, selected_skills):
    """Insert selected hobbies and skills into the database for the specified user."""
    try:
        # Create new UserHobbies entry
        new_hobbies = user_hobbies(
            user_id=user_id,
            main_hobby=selected_hobbies[0] if len(selected_hobbies) > 0 else None,
            additional_hobby_1=selected_hobbies[1] if len(selected_hobbies) > 1 else None,
            additional_hobby_2=selected_hobbies[2] if len(selected_hobbies) > 2 else None,
            additional_hobby_3=selected_hobbies[3] if len(selected_hobbies) > 3 else None,
        )
        db.session.add(new_hobbies)

        # Create new UserSkills entry
        new_skills = user_skills(
            user_id=user_id,
            main_skill=selected_skills[0] if len(selected_skills) > 0 else None,
            additional_skill_1=selected_skills[1] if len(selected_skills) > 1 else None,
            additional_skill_2=selected_skills[2] if len(selected_skills) > 2 else None,
            additional_skill_3=selected_skills[3] if len(selected_skills) > 3 else None,
        )
        db.session.add(new_skills)

        db.session.commit()  # Commit all changes
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        print("Error during commit:", e)
        flash('There was an error saving your hobbies and skills. Please try again.')



# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':  # Check if the form has been submitted
        # Retrieve email and password from the form data
        email = request.form['email']  # Get the email input from the form
        password = request.form['password']  # Get the password input from the form

        # Verify user credentials by querying the database
        user = User.query.filter_by(email=email).first()  # Find the user by email
        if user and check_password_hash(user.password, password):  # Validate password using hashed comparison
            # Store user ID in session for tracking user state
            session['user_id'] = user.user_id  # Save the user's ID in the session

            # Check if the user has taken the personality test by looking for their scores
            test_scores = PersonalityTestScores.query.filter_by(user_id=user.user_id).first()  # Query for test scores

            if not test_scores:  # If no test score exists for this user
                # If the user hasn't taken the test, reset question index and redirect to the personality test
                session['current_question_index'] = 0  # Reset to the first question of the personality test
                flash('Welcome! Please complete your personality test.')  # Flash a welcome message
                return redirect(url_for('personality_test'))  # Redirect to the personality test page

            # If test scores exist, proceed to the dashboard
            flash('Login successful!')  # Inform the user of successful login
            return redirect(url_for('dashboard'))  # Redirect to the dashboard page for logged-in users

        else:  # If user is not found or password is incorrect
            flash('Invalid credentials. Please try again.')  # Flash an error message
            return redirect(url_for('login'))  # Redirect back to the login page

    # If GET request, render the login template
    return render_template('login.html')  # Render the login form template

@app.route('/personality_test', methods=['GET', 'POST'])
def personality_test():
    """Handle the personality test process for the user."""
    # Retrieve the user ID and current question index from the session
    user_id = session.get('user_id')  # Get the logged-in user's ID from the session
    current_question_index = session.get('current_question_index', 0)  # Default to the first question if not set

    # Initialize category_scores in the session if not already present
    if 'category_scores' not in session:
        session['category_scores'] = {
            'E': 0,  # Score for Extraversion
            'I': 0,  # Score for Introversion
            'S': 0,  # Score for Sensing
            'N': 0,  # Score for Intuition
            'T': 0,  # Score for Thinking
            'F': 0,  # Score for Feeling
            'J': 0,  # Score for Judging
            'P': 0   # Score for Perceiving
        }

    category_scores = session['category_scores']  # Retrieve the category scores from the session

    # Initialize answers list in the session if not already present
    if 'answers' not in session:
        session['answers'] = []  # Create an empty list to store the user's answers

    answers = session['answers']  # Retrieve the answers list from the session

    if request.method == 'POST':  # Check if the form has been submitted
        answer_id = request.form.get('answer')  # Get the selected answer ID from the form
        print(f"Received answer ID: {answer_id}")  # Debugging output to track received answer ID

        # Ensure the answer ID is valid
        if answer_id:
            # Retrieve the selected answer from the database using the answer_id
            selected_answer = PersonalityTestAnswers.query.filter_by(answer_id=answer_id).first()
            if selected_answer:  # Check if the selected answer exists
                category = selected_answer.category  # Get the category for the selected answer
                if category in category_scores:  # Ensure the category is valid
                    # Increment the score for the selected category
                    category_scores[category] += 1

                    # Store the answer (including its index and text)
                    answers.append((current_question_index, selected_answer.answer_text))

                    # Update session data with the new scores and answers
                    session['category_scores'] = category_scores
                    session['answers'] = answers

                    # Move to the next question by incrementing the current question index
                    current_question_index += 1
                    session['current_question_index'] = current_question_index

                    # Check if all questions have been answered
                    total_questions = PersonalityTestQuestions.query.count()  # Get the total number of questions
                    if current_question_index >= total_questions:  # If the user has answered all questions
                        # Call the function to save the results to the database
                        save_personality_test_results(user_id=user_id, scores=category_scores)

                        # Clear session data to prepare for the next user
                        session.pop('current_question_index', None)  # Remove current question index from the session
                        session.pop('category_scores', None)  # Remove category scores from the session
                        session.pop('answers', None)  # Remove answers from the session
                        flash('Your test is complete!')  # Inform the user that the test is complete
                        return redirect(url_for('dashboard'))  # Redirect to the dashboard

                else:
                    # Log a warning if the category is not found in category_scores
                    print(f"Warning: Category '{category}' not in category_scores")
                    flash("Invalid answer category. Please try again.")  # Flash an error message
                    return redirect(url_for('personality_test'))  # Redirect back to the personality test

            else:
                # Log a warning if no valid answer is found for the provided ID
                print(f"Warning: No valid answer found for ID: {answer_id}")
                flash("Invalid answer submitted. Please try again.")  # Flash an error message
                return redirect(url_for('personality_test'))  # Redirect back to the personality test
        else:
            # Log a warning for invalid answer value
            print(f"Warning: Invalid answer value received: {answer_id}")
            flash("Please select a valid answer.")  # Flash an error message
            return redirect(url_for('personality_test'))  # Redirect back to the personality test

    # Retrieve the current question for the user
    current_question = PersonalityTestQuestions.query.offset(current_question_index).first()  # Get the current question
    if current_question:  # Check if a question was retrieved
        question_answers = PersonalityTestAnswers.query.filter_by(question_id=current_question.question_id).all()  # Get answers for the current question
    else:
        flash('No more questions available.')  # Notify user if there are no more questions
        return redirect(url_for('dashboard'))  # Redirect to the dashboard

    # Render the personality test template with the current question and its possible answers
    return render_template('personality_test.html', question=current_question, answers=question_answers)






def save_personality_test_results(user_id, scores):
    """Save personality test results for a user, updating existing scores or creating a new record."""
    # Check if a record exists for this user in the PersonalityTestScores table
    existing_result = db.session.query(PersonalityTestScores).filter_by(user_id=user_id).first()
    
    if existing_result:
        # If a record exists, update the scores by summing new scores with current ones
        for category, score in scores.items():  # Iterate through the score categories
            current_score = getattr(existing_result, category, 0)  # Get current score for the category, default to 0 if not found
            setattr(existing_result, category, current_score + score)  # Update the score by adding the new score
        db.session.commit()  # Commit the changes to the database
    else:
        # If no record exists, create a new entry in the PersonalityTestScores table
        new_result = PersonalityTestScores(user_id=user_id, **scores)  # Create a new instance with user ID and scores
        db.session.add(new_result)  # Add the new result to the session
        db.session.commit()  # Commit the changes to the database

    # Call the function to determine and store the dominant personality type based on scores
    determine_dominant_personality(user_id)




def determine_dominant_personality(user_id):
    """Determine the dominant personality type based on the user's scores and store the results."""
    # Fetch the scores for the user from the PersonalityTestScores table
    scores = db.session.query(PersonalityTestScores).filter_by(user_id=user_id).first()
    
    if scores:
        # Initialize a dictionary to hold the dominant personality types
        dominant_types = {}

        # Determine the primary personality type between Thinking (T) and Feeling (F)
        if scores.T > scores.F:
            dominant_types['primary_personality_type'] = 'T'  # Thinking is dominant
        else:
            dominant_types['primary_personality_type'] = 'F'  # Feeling is dominant

        # Determine the alternative personality type between Sensing (S) and Intuition (N)
        if scores.S > scores.N:
            dominant_types['alternative_1'] = 'S'  # Sensing is dominant
        else:
            dominant_types['alternative_1'] = 'N'  # Intuition is dominant

        # Determine the alternative personality type between Extraversion (E) and Introversion (I)
        if scores.E > scores.I:
            dominant_types['alternative_2'] = 'E'  # Extraversion is dominant
        else:
            dominant_types['alternative_2'] = 'I'  # Introversion is dominant

        # Determine the alternative personality type between Judging (J) and Perceiving (P)
        if scores.J > scores.P:
            dominant_types['alternative_3'] = 'J'  # Judging is dominant
        else:
            dominant_types['alternative_3'] = 'P'  # Perceiving is dominant

        # Check if a record exists for the user's dominant personality types
        existing_result = db.session.query(user_personality_types).filter_by(user_id=user_id).first()
        
        if existing_result:
            # If a record exists, update it with the new dominant personality types
            for key, value in dominant_types.items():  # Iterate through the dominant types
                setattr(existing_result, key, value)  # Update the corresponding field in the existing record
            db.session.commit()  # Commit the changes to the database
        else:
            # If no record exists, create a new entry in the user_personality_types table
            new_result = user_personality_types(user_id=user_id, **dominant_types)  # Create a new instance with user ID and dominant types
            db.session.add(new_result)  # Add the new result to the session
            db.session.commit()  # Commit the changes to the database






@app.route('/dashboard')
def dashboard():
    """Render the dashboard for logged-in users or redirect to login if not authenticated."""
    user_id = session.get('user_id')  # Get the user ID from the session
    if user_id:  # Check if the user is logged in
        user = db.session.get(User, user_id)  # Fetch the user object from the database
        # Here you can fetch any additional data needed for the dashboard
        return render_template('dashboard.html', user=user)  # Render the dashboard template with user data
    else:
        flash('Please log in to view your dashboard.')  # Flash message for unauthorized access
        return redirect(url_for('login'))  # Redirect to the login page if not logged in



# Home route
@app.route('/home')
def home():
    """Render the home page for logged-in users or redirect to login if not authenticated."""
    user_id = session.get('user_id')  # Get the user ID from the session
    if user_id:  # Check if the user is logged in
        user = db.session.get(User, user_id)  # Fetch the user object from the database
        return render_template('home.html', user=user)  # Render the home template with user data
    else:
        flash('Please log in to continue.')  # Flash message for unauthorized access
        return redirect(url_for('login'))  # Redirect to the login page if not logged in




# Logout route
@app.route('/logout')
def logout():
    """Log out the user by clearing the session and redirect to the login page."""
    session.clear()  # Clear the session data
    flash('You have been logged out.')  # Flash message confirming logout
    return redirect(url_for('login'))  # Redirect to the login page after logging out





@app.route('/results')
def results():
    """Display the user's personality test results if logged in, or redirect to login."""
    user_id = session.get('user_id')  # Get the user ID from the session
    if user_id:  # Check if the user is logged in
        # Fetch user's personality test scores from the database
        scores = PersonalityTestScores.query.filter_by(user_id=user_id).first()
        personality_type = user_personality_types.query.filter_by(user_id=user_id).first()

        if scores and personality_type:  # Check if scores and personality type exist
            # Prepare data for the results template
            result_data = {
                'E': scores.E,
                'I': scores.I,
                'S': scores.S,
                'N': scores.N,
                'T': scores.T,
                'F': scores.F,
                'J': scores.J,
                'P': scores.P,
                'primary_personality_type': personality_type.primary_personality_type,
                'alternative_1': personality_type.alternative_1,
                'alternative_2': personality_type.alternative_2,
                'alternative_3': personality_type.alternative_3
            }
            return render_template('results.html', result_data=result_data)  # Render results template with data
        else:
            flash('You have not completed the personality test yet.')  # Flash message if test is incomplete
            return redirect(url_for('dashboard'))  # Redirect to the dashboard if test is incomplete
    else:
        flash('Please log in to view your results.')  # Flash message for unauthorized access
        return redirect(url_for('login'))  # Redirect to the login page if not logged in





@app.route('/recommended_jobs')
def recommended_jobs():
    """Render the recommended jobs page."""
    # Logic to retrieve recommended jobs can be added here
    return render_template('recommended_jobs.html')  # Render the recommended jobs template





@app.route('/recommended_courses')
def recommended_courses():
    """Render the recommended courses page."""
    # Logic to retrieve recommended courses can be added here
    return render_template('recommended_courses.html')  # Render the recommended courses template





@app.route('/recommended_schools')
def recommended_schools():
    """Render the recommended schools page."""
    # Logic to retrieve recommended schools can be added here
    return render_template('recommended_schools.html')  # Render the recommended schools template





@app.route('/cv_creator')
def cv_creator():
    """Render the CV creation page."""
    # Logic to implement CV creation can be added here
    return render_template('cv_creator.html')  # Render the CV creator template






@app.route('/account_details')
def account_details():
    """Render the user account details page."""
    # Logic to retrieve user account details can be added here
    return render_template('account_details.html')  # Render the account details template




@app.route('/chat_help')
def chat_help():
    """Render the chat help page."""
    # Logic for chat help can be added here
    return render_template('chat_help.html')  # Ensure you have a corresponding HTML file




# Main entry point for the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they do not exist
    app.run(debug=True)  # Run the application in debug mode
