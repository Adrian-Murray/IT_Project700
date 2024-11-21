from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.String(200))
    career_interests = db.Column(db.String(200))
    password = db.Column(db.LargeBinary, nullable=False)
    reference_profile_id = db.Column(db.Integer, db.ForeignKey('reference_profiles.id'))
    course = db.Column(db.String(100))
    university_id = db.Column(db.String(10))
    faculty = db.Column(db.String(100))
    duration = db.Column(db.Integer)

class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    tel_number = db.Column(db.String) 
    website = db.Column(db.String)    

class Career(db.Model):
    __tablename__ = 'careers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    required_skills = db.Column(db.String(200))  
    description = db.Column(db.Text)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    credits = db.Column(db.Integer)
    university_id = db.Column(db.String(10))  
    faculty = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    recommended_career = db.Column(db.String(100))
    key_skills = db.Column(db.String(200))

class Mentorship(db.Model):
    __tablename__ = 'mentorships'
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mentee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mentor = db.relationship('User', foreign_keys=[mentor_id])
    mentee = db.relationship('User', foreign_keys=[mentee_id])

class CVTemplate(db.Model):
    __tablename__ = 'cv_templates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    template_url = db.Column(db.String(200))  

class ReferenceProfile(db.Model):
    __tablename__ = 'reference_profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    dominance = db.Column(db.Integer)
    extraversion = db.Column(db.Integer)
    patience = db.Column(db.Integer)
    formality = db.Column(db.Integer)


class BehavioralAssessment(db.Model):
    __tablename__ = 'behavioral_assessments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_type = db.Column(db.String(50))  # "Expected" or "Self-description"
    adjective = db.Column(db.String(50))
    factor = db.Column(db.String(50))  # "Dominance", "Extraversion", "Patience", "Formality" 

