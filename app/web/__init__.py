"""
Web Routes Package

This package contains routes for serving web pages.
"""

from flask import Blueprint

# Create web blueprint
web_bp = Blueprint('web', __name__)

# Import routes to register them with the blueprint
from app.web import routes

__all__ = ['web_bp']

