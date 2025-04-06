"""Configuration module for the AI Travel Assistant."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# API Keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')

# Server Configuration
BACKEND_HOST = os.getenv('BACKEND_HOST', '127.0.0.1')
BACKEND_PORT = int(os.getenv('BACKEND_PORT', '8000'))
FRONTEND_PORT = int(os.getenv('FRONTEND_PORT', '7860'))

# Application Settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

def validate_config():
    """Validate that required configuration is present."""
    if not GOOGLE_API_KEY and not DEEPSEEK_API_KEY:
        print("WARNING: Neither GOOGLE_API_KEY nor DEEPSEEK_API_KEY is set. The application will not function correctly without a valid API key.")
        return False
    return True
