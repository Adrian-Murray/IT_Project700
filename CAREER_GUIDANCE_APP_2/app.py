from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
import datetime
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

# Configure the SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'resource/users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.String(100), nullable=False)
    education_level = db.Column(db.String(100), nullable=False)



class PersonalityTestQuestions(db.Model):
    __tablename__ = 'PersonalityTestQuestions'
    question_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)

class PersonalityTestAnswers(db.Model):
    __tablename__ = 'PersonalityTestAnswers'
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('PersonalityTestQuestions.question_id'), nullable=False)
    answer_text = db.Column(db.String(100), nullable=False)
    answer_value = db.Column(db.String(1), nullable=False)  # Changed to one character

class PersonalityTestScores(db.Model):
    __tablename__ = 'PersonalityTestScores'
    score_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    category = db.Column(db.String(1), nullable=False)  # 'E', 'I', etc.
    score = db.Column(db.Integer, nullable=False)

# Validation Helper Functions
def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def is_valid_name(name):
    return re.match(r'^[A-Za-z]+$', name)

def is_valid_mobile_number(mobile_number):
    # This validation checks for a 10 to 15-digit phone number with or without a '+' prefix
    if mobile_number.startswith('+'):
        return re.match(r'^\+[0-9]{10,15}$', mobile_number)
    else:
        return re.match(r'^[0-9]{10,15}$', mobile_number)

def is_valid_date_of_birth(date_of_birth):
    try:
        birth_date = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')
        today = datetime.datetime.today()
        # Check if date_of_birth is in the past and user is at least 10 years old
        age = (today - birth_date).days // 365
        return birth_date < today and age >= 10
    except ValueError:
        return False

def is_valid_education(education_level):
    valid_education_levels = ['Matric', 'University', 'Grade 10 or below']
    return education_level in valid_education_levels

# Index route
@app.route('/')
def index():
    return redirect(url_for('home'))

# Sign-up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']  # In production, hash the password
        name = request.form['name']
        surname = request.form['surname']
        mobile_number = request.form['mobile_number']
        date_of_birth = request.form['date_of_birth']
        education_level = request.form['education_level']

        # Perform validation checks
        if not is_valid_email(email):
            flash('Invalid email format.')
            return redirect(url_for('signup'))
        
        if not is_valid_name(name) or not is_valid_name(surname):
            flash('Name and surname should not contain numbers or special characters.')
            return redirect(url_for('signup'))
        
        if not is_valid_mobile_number(mobile_number):
            flash('Invalid mobile number format.')
            return redirect(url_for('signup'))
        
        if not is_valid_date_of_birth(date_of_birth):
            flash('Invalid date of birth. Ensure it\'s in YYYY-MM-DD format and you are above 10 years old.')
            return redirect(url_for('signup'))
        
        if not is_valid_education(education_level):
            flash('Please select a valid education level.')
            return redirect(url_for('signup'))

        # Check if the user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists. Please log in.')
            return redirect(url_for('login'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create new user and add to the database
        new_user = User(email=email, password=hashed_password, name=name, surname=surname,
                        mobile_number=mobile_number, date_of_birth=date_of_birth, education_level=education_level)
        db.session.add(new_user)
        db.session.commit()
        flash('Sign up successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/view_results')
def view_results():
    # Logic to retrieve user results can be added here
    return render_template('view_results.html')

@app.route('/recommended_jobs')
def recommended_jobs():
    # Logic to retrieve recommended jobs can be added here
    return render_template('recommended_jobs.html')

@app.route('/recommended_courses')
def recommended_courses():
    # Logic to retrieve recommended courses can be added here
    return render_template('recommended_courses.html')

@app.route('/recommended_schools')
def recommended_schools():
    # Logic to retrieve recommended schools can be added here
    return render_template('recommended_schools.html')

@app.route('/cv_creator')
def cv_creator():
    # Logic to implement CV creation can be added here
    return render_template('cv_creator.html')

@app.route('/account_details')
def account_details():
    # Logic to retrieve user account details can be added here
    return render_template('account_details.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verify user credentials
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id  # Store user ID in session

            # Check if user has taken the test by looking for their scores
            test_scores = PersonalityTestScores.query.filter_by(user_id=user.user_id).first()
            
            if not test_scores:
                # If no test score exists, reset question index and redirect to the personality test
                session['current_question_index'] = 0  # Reset to the first question
                return redirect(url_for('personality_test'))

            flash('Login successful!')
            return redirect(url_for('dashboard'))  # User already completed the test, go to dashboard
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')




# Add this model for storing final personality test results
class PersonalityTestResults(db.Model):
    __tablename__ = 'PersonalityTestResults'
    result_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    question_id = db.Column(db.Integer, db.ForeignKey('PersonalityTestQuestions.question_id'))
    answer = db.Column(db.String(1), nullable=False)  # Restricting to one character

# Update the personality_test route
@app.route('/personality_test', methods=['GET', 'POST'])
def personality_test():
    user_id = session.get('user_id')

    # Initialize or retrieve current question index from session
    current_question_index = session.get('current_question_index', 0)

    # Retrieve or initialize category scores from session
    category_scores = session.get('category_scores', {
        'E': 0,
        'I': 0,
        'S': 0,
        'N': 0,
        'T': 0,
        'F': 0,
        'J': 0,
        'P': 0
    })

    # Retrieve or initialize answers list from session
    answers = session.get('answers', [])

    if request.method == 'POST':
        # Update category scores and store the answer
        answer_value = request.form.get('answer')
        if answer_value:
            if answer_value in category_scores:
                category_scores[answer_value] += 1
                answers.append((user_id, current_question_index, answer_value))

            session['category_scores'] = category_scores
            session['answers'] = answers

        # Increment question index and update session
        current_question_index += 1
        session['current_question_index'] = current_question_index

        # Check total questions
        total_questions = PersonalityTestQuestions.query.count()
        if current_question_index >= total_questions:
            save_results(user_id, category_scores, answers)

            session.pop('current_question_index', None)
            session.pop('category_scores', None)
            session.pop('answers', None)

            flash('Your test is complete!')
            return redirect(url_for('dashboard'))

    # Fetch the current question
    current_question = PersonalityTestQuestions.query.offset(current_question_index).first()

    # Ensure current_question is found
    if current_question:
        question_answers = PersonalityTestAnswers.query.filter_by(question_id=current_question.question_id).all()
        print("Current Question:", current_question)
        print("Question Answers:", question_answers)  # Debugging line to check fetched answers
    else:
        question_answers = []

        # Redirect if no more questions
        flash('No more questions available.')
        return redirect(url_for('dashboard'))

    return render_template('personality_test.html', question=current_question, answers=question_answers)



# Update the save_results function
def save_results(user_id, category_scores, answers):
    # Loop through each category score and save it
    for category, score in category_scores.items():
        # Check if there's an existing score for the user and category
        existing_score = (
            PersonalityTestScores.query
            .filter_by(user_id=user_id, category=category)
            .first()
        )
        if existing_score:
            # Update the existing score
            existing_score.score += score  # You might want to adjust how scores are summed
        else:
            # Create a new score record
            new_score = PersonalityTestScores(
                user_id=user_id,
                category=category,
                score=score
            )
            db.session.add(new_score)
    
    # Commit the session after all operations
    db.session.commit()




def determine_category_for_answer(answer_value):
    # Query the database to find the category associated with the answer_value
    answer_record = PersonalityTestAnswers.query.filter_by(answer=answer_value).first()
    
    # Check if the answer_record is found and return the category
    if answer_record:
        return answer_record.category  # Assuming category is in the PersonalityTestAnswers table
    else:
        print(f"Warning: No category found for answer_value: {answer_value}")  # Log a warning for debugging
        return None  # Return None if no category is found


@app.route('/calculate_results', methods=['POST'])
def calculate_results():
    user_id = session.get('user_id')

    # Fetch all answers from the session
    user_answers = session.get('user_answers', {})  # Assuming answers are stored in session
    # Initialize counters for each pair of categories
    score = {
        'E': 0, 'I': 0,  # Extraversion vs Introversion
        'S': 0, 'N': 0,  # Sensing vs Intuition
        'T': 0, 'F': 0,  # Thinking vs Feeling
        'J': 0, 'P': 0   # Judging vs Perceiving
    }

    # Loop through the user's answers and count each category selection
    for question_id, answer_category in user_answers.items():
        # Update the corresponding score for the selected category
        if answer_category in score:
            score[answer_category] += 1

    # Check if the user already has entries in PersonalityTestScores and update them
    existing_scores = PersonalityTestScores.query.filter_by(user_id=user_id).all()
    if existing_scores:
        # If the user already has test scores, update them
        for test_score in existing_scores:
            test_score.score = score[test_score.category]
    else:
        # If no scores exist for this user, create new entries
        for category, category_score in score.items():
            new_score = PersonalityTestScores(
                user_id=user_id,
                category=category,
                score=category_score
            )
            db.session.add(new_score)

    # Commit the results to the database
    db.session.commit()

    # Flash message and redirect to the dashboard
    flash('Test completed successfully! Your results have been saved.')
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        # Here you can fetch any additional data needed for the dashboard
        return render_template('dashboard.html', user=user)
    else:
        flash('Please log in to view your dashboard.')
        return redirect(url_for('login'))

def save_results(user_id, category_scores, answers):
    # Save the results based on the largest score category for each question
    for question_id, answer in answers:  # Assuming answers is a list of tuples (question_id, answer)
        # Get the answer from the PersonalityTestAnswers table to determine the correct category
        answer_record = PersonalityTestAnswers.query.filter_by(question_id=question_id, answer_value=answer).first()
        
        if answer_record:
            category = answer_record.answer_value  # Assuming this gives you the category (e.g., 'E', 'I')
            # Save the result directly to PersonalityTestScores
            existing_score = PersonalityTestScores.query.filter_by(user_id=user_id, category=category).first()
            
            if existing_score:
                # If a score for this category already exists, update it
                existing_score.score += 1  # Increment the score, or however you want to aggregate it
            else:
                # If no score exists for this category, create a new entry
                new_score = PersonalityTestScores(user_id=user_id, category=category, score=1)  # Start with a score of 1
                db.session.add(new_score)

    # Commit the results to the database
    db.session.commit()


# Home route
@app.route('/home')
def home():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return render_template('home.html', user=user)
    else:
        flash('Please log in to continue.')
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
