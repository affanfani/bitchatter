"""
Testing Configuration

This module contains testing-specific configuration settings.
"""

from .base import BaseConfig


class TestingConfig(BaseConfig):
    """Testing configuration"""
    
    DEBUG = True
    TESTING = True
    
    # Testing-specific settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False
    LOG_LEVEL = 'ERROR'
    
    # Disable external API calls during testing
    OPENROUTER_API_KEY = 'test-key'
