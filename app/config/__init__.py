"""
Configuration Package

This package contains configuration classes for different environments
(development, testing, production).
"""

from .base import BaseConfig
from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

__all__ = ['config', 'BaseConfig', 'DevelopmentConfig', 'ProductionConfig', 'TestingConfig']
