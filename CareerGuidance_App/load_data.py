from flask import Flask, jsonify, request
import csv
from extensions import db
from app import app
from models import ReferenceProfile, University, Course

with app.app_context():
    db.create_all()

def load_reference_profiles():
    with open('data/reference_profiles.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        print("Detected headers for reference profiles:", reader.fieldnames)

        for row in reader:
            if row.get("Profiles"):
                profile = ReferenceProfile(
                    name=row.get("Profiles"),
                    description=row.get("Description", ""),
                    dominance=int(row.get("Dominance", 0)) if row.get("Dominance") else None,
                    extraversion=int(row.get("Extraversion", 0)) if row.get("Extraversion") else None,
                    patience=int(row.get("Patience", 0)) if row.get("Patience") else None,
                    formality=int(row.get("Formality", 0)) if row.get("Formality") else None
                )
                db.session.add(profile)

        db.session.commit()
    print("Reference profiles loaded successfully.")

def load_universities():
    with open('data/universities.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not University.query.filter_by(id=row["ID"]).first():
                university = University(
                    id=row["ID"],
                    name=row["Name"],
                    tel_number=row["Tel Number"],
                    website=row["Website"]
                )
                db.session.add(university)
        db.session.commit()
    print("Universities loaded successfully.")

# Load Courses
def load_courses():
    with open('data/courses_cleaned.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=';')
        print("Detected headers for courses:", reader.fieldnames)

        for row in reader:
            if row.get("Course"):
                try:

                    course = Course(
                        name=row["Course"].strip(),
                        university_id=row["Universities_ID"].strip(),
                        faculty=row["Faculty/Derpatment"].strip(),
                        duration=int(row["Duration"].strip()) if row["Duration"].strip().isdigit() else None,
                        recommended_career=row["Recommended Career"].strip(),
                        key_skills=row["Key Skills"].strip()
                    )
                    db.session.add(course)
                except Exception as e:
                    print(f"Error loading row {row}: {e}")

        try:
            db.session.commit()
            print("Courses loaded successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"Error committing courses to the database: {e}")

with app.app_context():
    load_reference_profiles()
    load_universities()
    load_courses()

    courses = Course.query.all()
    print(f"Total courses loaded: {len(courses)}")
    for course in courses:
        print(course.name, course.university_id, course.faculty, course.duration)
