"""
Base Configuration

This module contains the base configuration class with common settings
shared across all environments.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # OpenRouter Configuration
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY') or os.environ.get('OpenAPI')
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL = os.environ.get('OPENROUTER_MODEL', 'meta-llama/llama-3.3-70b-instruct:free')
    
    # Site Information
    SITE_URL = os.environ.get('SITE_URL', 'http://localhost:5000')
    SITE_NAME = os.environ.get('SITE_NAME', 'University Department Chatbot')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', 60))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # API Configuration
    API_TITLE = "University Department Chatbot API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "API documentation for the University Department Chatbot"
