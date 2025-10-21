"""
Flask Application Factory

This module contains the Flask application factory function that creates
and configures the Flask application instance.
"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS

from app.config import config
from app.config.swagger_config import init_swagger
from app.database import db
from app.utils.exceptions import APIException


def create_app(config_name=None):
    """
    Flask application factory.
    
    Args:
        config_name: Configuration name (development, production, testing)
        
    Returns:
        Configured Flask application
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Configure logging
    configure_logging(app)
    
    # Initialize extensions
    init_extensions(app)
    
    # Initialize Swagger documentation
    init_swagger(app)
    
    # Register API blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            "message": "University Department Chatbot API",
            "documentation": "/apidocs",
            "api": {
                "root": "/api",
                "v1": "/api/v1",
                "health": "/api/v1/health",
                "chat": "/api/v1/chat/message"
            }
        })
    
    return app


def configure_logging(app):
    """Configure application logging"""
    if not app.debug and not app.testing:
        logging.basicConfig(
            level=getattr(logging, app.config.get('LOG_LEVEL', 'INFO')),
            format='%(asctime)s %(levelname)s %(name)s - %(message)s'
        )


def init_extensions(app):
    """Initialize Flask extensions"""
    # Initialize database
    db.init_app(app)
    
    # Initialize CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))


def register_blueprints(app):
    """Register API blueprints"""
    from app.api.api import register_api_blueprints
    register_api_blueprints(app)


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(APIException)
    def handle_api_exception(e):
        return jsonify({
            "error": e.message,
            "details": e.details,
            "status_code": e.status_code
        }), e.status_code
    
    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            "error": "Not found",
            "message": "The requested resource was not found",
            "status_code": 404
        }), 404
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "status_code": 500
        }), 500
