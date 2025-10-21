"""
Development Configuration

This module contains development-specific configuration settings.
"""

from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    
    DEBUG = True
    TESTING = False
    
    # Development-specific settings
    SQLALCHEMY_ECHO = True
    LOG_LEVEL = 'DEBUG'
