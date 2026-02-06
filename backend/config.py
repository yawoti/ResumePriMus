import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""

    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Claude API settings
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

    # File upload settings
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 5242880))  # 5MB default
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'pdf,docx,txt').split(','))
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.CLAUDE_API_KEY:
            raise ValueError("CLAUDE_API_KEY environment variable is required")
