"""
Production Configuration

This module contains production-specific configuration settings.
"""

from .base import BaseConfig


class ProductionConfig(BaseConfig):
    """Production configuration"""
    
    DEBUG = False
    TESTING = False
    
    # Production-specific settings
    SQLALCHEMY_ECHO = False
    LOG_LEVEL = 'WARNING'
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
