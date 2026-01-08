import os
from dotenv import load_dotenv
from typing import Dict, Any
import logging
from logging.handlers import RotatingFileHandler
import sys

# Load environment variables
load_dotenv()

# API Keys
API_KEYS = {
    'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
    'RESEND_API_KEY': os.getenv('RESEND_API_KEY'),
    'WEATHER_API_KEY': os.getenv('WEATHER_API_KEY')
}

# Validate API keys
for key, value in API_KEYS.items():
    if not value:
        raise ValueError(f"{key} environment variable is not set")

# Application settings
APP_CONFIG = {
    'WINDOW_TITLE': 'AI Assistant',
    'WINDOW_SIZE': '500x650',
    'WINDOW_RESIZABLE': False,
    'BACKGROUND_COLOR': '#F4F4F9',
    'HEADER_COLOR': '#4A90E2',
    'BUTTON_COLOR': '#4CAF50',
    'TEXT_COLOR': '#333333',
    'RESPONSE_BG_COLOR': '#E8EAF6'
}

# Speech settings
SPEECH_CONFIG = {
    'SPEECH_RATE': 130,
    'SPEECH_VOLUME': 1.0,
    'SPEECH_TIMEOUT': 5,
    'SPEECH_PHRASE_TIME_LIMIT': 5
}

# Weather settings
WEATHER_CONFIG = {
    'MIN_REQUEST_INTERVAL': 1,  # seconds
    'REQUEST_TIMEOUT': 10,      # seconds
    'UNITS': 'metric'
}

# Email settings
EMAIL_CONFIG = {
    'DEFAULT_SENDER': 'onboarding@resend.dev',
    'MAX_RETRIES': 3,
    'RETRY_DELAY': 1  # seconds
}

# Logging settings
LOGGING_CONFIG = {
    'LOG_FILE': 'assistant.log',
    'LOG_LEVEL': 'INFO',
    'LOG_FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'MAX_BYTES': 5 * 1024 * 1024,  # 5MB
    'BACKUP_COUNT': 3
}

def setup_logging():
    """
    Set up logging configuration for the application.
    Creates rotating file handler to manage log file size.
    """
    try:
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Configure root logger
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, LOGGING_CONFIG['LOG_LEVEL']))
        
        # Remove any existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Create rotating file handler
        log_file = os.path.join(logs_dir, LOGGING_CONFIG['LOG_FILE'])
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=LOGGING_CONFIG['MAX_BYTES'],
            backupCount=LOGGING_CONFIG['BACKUP_COUNT'],
            encoding='utf-8'
        )
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        
        # Create formatter
        formatter = logging.Formatter(LOGGING_CONFIG['LOG_FORMAT'])
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Log initial message
        logger.info("Logging system initialized")
        
        return logger
        
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        # Fallback to basic logging
        logging.basicConfig(
            level=logging.INFO,
            format=LOGGING_CONFIG['LOG_FORMAT']
        )
        return logging.getLogger()

def get_config() -> Dict[str, Any]:
    """
    Get the complete configuration.
    
    Returns:
        Dict[str, Any]: The complete configuration dictionary
    """
    return {
        'API_KEYS': API_KEYS,
        'APP_CONFIG': APP_CONFIG,
        'SPEECH_CONFIG': SPEECH_CONFIG,
        'WEATHER_CONFIG': WEATHER_CONFIG,
        'EMAIL_CONFIG': EMAIL_CONFIG,
        'LOGGING_CONFIG': LOGGING_CONFIG
    } 