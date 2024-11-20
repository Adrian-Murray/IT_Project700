import os
import logging
from logging.handlers import RotatingFileHandler

class Config:
    # Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    
    # Database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Logging config
    LOG_FOLDER = 'logs'
    LOG_FILENAME = 'app.log'
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_MAX_BYTES = 10_000_000  # 10MB
    LOG_BACKUP_COUNT = 5

    @staticmethod
    def init_logging(app):
        # Create logs directory if it doesn't exist
        if not os.path.exists(Config.LOG_FOLDER):
            os.makedirs(Config.LOG_FOLDER)

        # Configure logging
        formatter = logging.Formatter(Config.LOG_FORMAT)
        
        # File handler
        file_handler = RotatingFileHandler(
            os.path.join(Config.LOG_FOLDER, Config.LOG_FILENAME),
            maxBytes=Config.LOG_MAX_BYTES,
            backupCount=Config.LOG_BACKUP_COUNT
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(Config.LOG_LEVEL)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(Config.LOG_LEVEL)
        
        # Root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(Config.LOG_LEVEL)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        # Werkzeug logger
        logging.getLogger('werkzeug').setLevel(logging.INFO)

    TEST_CONFIG = {
    "host": "http://localhost:5000",
    "test_user": {
        "email": "test@example.com",
        "password": "test123"
    },
    "load_test": {
        "duration": 300,  # 5 minutes
        "users": 100,
        "spawn_rate": 10
    },
    "stress_test": {
        "num_requests": 1000,
        "max_workers": 50
    }
}