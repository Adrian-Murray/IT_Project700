# verify_db.py
from app import app
from models import ReferenceProfile, University, Course

def verify_database():
    with app.app_context():
        # Check Reference Profiles
        profiles = ReferenceProfile.query.all()
        print(f"\nReference Profiles: {len(profiles)}")
        if profiles:
            print("Sample profile:", profiles[0].name)
        
        # Check Universities
        universities = University.query.all()
        print(f"\nUniversities: {len(universities)}")
        if universities:
            print("Sample university:", universities[0].name)
        
        # Check Courses
        courses = Course.query.all()
        print(f"\nCourses: {len(courses)}")
        if courses:
            print("Sample course:", courses[0].name)

if __name__ == "__main__":
    verify_database()