"""
API Entry Point

This module serves as the entry point for all API routes.
It registers versioned API blueprints (v1, v2, etc.) with proper URL prefixes.

Following best practices for API versioning:
- Each version has its own blueprint and namespace
- Versions are isolated and can evolve independently
- URL structure: /api/v1/, /api/v2/, etc.
"""

from flask import Blueprint, jsonify

# Create main API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/', methods=['GET'])
def api_root():
    """
    API Root Endpoint
    ---
    tags:
      - General
    responses:
      200:
        description: API information and available versions
        schema:
          type: object
          properties:
            message:
              type: string
              example: "University Department Chatbot API"
            versions:
              type: object
              properties:
                v1:
                  type: object
                  properties:
                    status:
                      type: string
                      example: "active"
                    endpoints:
                      type: string
                      example: "/api/v1"
            documentation:
              type: string
              example: "/apidocs"
    """
    return jsonify({
        "message": "University Department Chatbot API",
        "versions": {
            "v1": {
                "status": "active",
                "endpoints": "/api/v1",
                "health": "/api/v1/health",
                "status_url": "/api/v1/status"
            }
        },
        "documentation": "/apidocs"
    }), 200


def register_api_blueprints(app):
    """
    Register all API version blueprints with the Flask app.
    
    This function centralizes API blueprint registration, making it easy to:
    - Add new API versions
    - Deprecate old versions
    - Maintain versioned endpoints
    
    Args:
        app: Flask application instance
    """
    # Import and register v1 blueprint to api_bp BEFORE registering api_bp to app
    from app.api.v1 import bp as v1_bp
    api_bp.register_blueprint(v1_bp, url_prefix='/v1')
    
    # Future versions can be added here:
    # from app.api.v2 import bp as v2_bp
    # api_bp.register_blueprint(v2_bp, url_prefix='/v2')
    
    # Now register the main API blueprint to the app
    app.register_blueprint(api_bp)


__all__ = ['api_bp', 'register_api_blueprints']

