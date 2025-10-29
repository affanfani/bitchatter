"""
Flask Application Factory

This module contains the Flask application factory function that creates
and configures the Flask application instance.
"""

import os
import logging
from pathlib import Path
from flask import Flask, jsonify
from flask_cors import CORS

from app.config import config
from app.config.swagger_config import init_swagger
from app.database import db
from app.utils.exceptions import APIException
from app.utils.vector_db import build_index_from_intents, FAISSVectorDB


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
    
    # Initialize vector database
    init_vector_db(app)
    
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


def init_vector_db(app):
    """Initialize vector database on startup"""
    logger = logging.getLogger(__name__)
    
    # Get paths
    base_dir = Path(__file__).parent.parent
    data_path = base_dir / 'data' / 'Ibit_data.json'
    vector_db_dir = base_dir / 'data' / 'vector_db'
    
    # Check if vector DB already exists
    index_path = vector_db_dir / 'faiss.index'
    metadata_path = vector_db_dir / 'metadata.pkl'
    config_path = vector_db_dir / 'config.json'
    
    if index_path.exists() and metadata_path.exists() and config_path.exists():
        logger.info("Vector database already exists, loading existing index")
        try:
            vector_db = FAISSVectorDB()
            vector_db.load(str(index_path), str(metadata_path), str(config_path))
            stats = vector_db.get_stats()
            logger.info(f"Loaded vector database with {stats['total_vectors']} vectors")
            
            # Store in app config for later use
            app.config['VECTOR_DB'] = vector_db
            return vector_db
        except Exception as e:
            logger.warning(f"Failed to load existing vector database: {e}")
            logger.info("Will rebuild vector database")
    
    # Build new vector database
    if not data_path.exists():
        logger.error(f"Data file not found: {data_path}")
        logger.warning("Skipping vector database initialization")
        return None
    
    try:
        logger.info("=" * 60)
        logger.info("Building FAISS Vector Database")
        logger.info("=" * 60)
        logger.info(f"Input file: {data_path}")
        logger.info(f"Output directory: {vector_db_dir}")
        
        # Build the index
        vector_db = build_index_from_intents(
            json_path=str(data_path),
            output_dir=str(vector_db_dir),
            model_name='all-MiniLM-L6-v2',
            batch_size=32
        )
        
        # Print statistics
        stats = vector_db.get_stats()
        logger.info("=" * 60)
        logger.info("Vector Database Statistics:")
        logger.info(f"  Total vectors: {stats['total_vectors']}")
        logger.info(f"  Dimension: {stats['dimension']}")
        logger.info(f"  Model: {stats['model_name']}")
        logger.info(f"  Metadata entries: {stats['metadata_count']}")
        logger.info("=" * 60)
        logger.info("✓ Vector database built successfully!")
        
        # Store in app config for later use
        app.config['VECTOR_DB'] = vector_db
        return vector_db
        
    except Exception as e:
        logger.error(f"Error building vector database: {e}", exc_info=True)
        logger.warning("Continuing without vector database")
        return None


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
