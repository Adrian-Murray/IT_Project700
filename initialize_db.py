import traceback
from app import app, db
from models import ReferenceProfile
import logging

logger = logging.getLogger(__name__)

def init_database():
    with app.app_context():
        try:
            # Drop all tables
            db.drop_all()
            logger.info("Dropped all existing tables")

            # Create all tables
            db.create_all()
            logger.info("Created all tables")

            # Create default reference profiles
            profiles = [
                ReferenceProfile(
                    name="Leader",
                    description="Natural leader with strong decision-making skills",
                    dominance=8,
                    extraversion=7,
                    patience=4,
                    formality=6
                ),
                ReferenceProfile(
                    name="Analyst",
                    description="Detail-oriented problem solver",
                    dominance=5,
                    extraversion=4,
                    patience=7,
                    formality=9
                ),
                ReferenceProfile(
                    name="Collaborator",
                    description="Team player with strong interpersonal skills",
                    dominance=4,
                    extraversion=8,
                    patience=8,
                    formality=5
                )
            ]

            for profile in profiles:
                db.session.add(profile)
            
            db.session.commit()
            logger.info("Created default reference profiles")

        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            logger.error(traceback.format_exc())
            db.session.rollback()

if __name__ == "__main__":
    init_database()