"""
Swagger/Flasgger Configuration

This module provides Swagger/OpenAPI documentation configuration
for the Flask application using Flasgger.
"""

from flasgger import Swagger


# Swagger UI configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

# OpenAPI specification template
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "University Department Chatbot API",
        "description": "API documentation for the University Department Chatbot - A Flask application for learning LLM integration",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "url": "https://github.com/affanfani/bitchatter"
        }
    },
    "basePath": "/",
    "schemes": ["http", "https"]
}


def init_swagger(app):
    """
    Initialize Swagger documentation for the Flask app.
    
    Args:
        app: Flask application instance
        
    Returns:
        Swagger instance
    """
    return Swagger(app, config=swagger_config, template=swagger_template)
