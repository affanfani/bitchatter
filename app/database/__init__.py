"""
Database Package

This package contains database configuration and models.
"""

from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy instance
db = SQLAlchemy()

__all__ = ['db']
