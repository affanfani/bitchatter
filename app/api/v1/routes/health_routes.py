"""
Health Check API Routes

This module contains health check and status endpoints for version 1.
"""

from flask import jsonify, current_app
from flasgger import swag_from
from app.api.v1 import bp
from app.core.llm_engine import create_llm_engine
from app.database import db
import logging
import psutil
import platform
from datetime import datetime

logger = logging.getLogger(__name__)


@bp.route('/health', methods=['GET'])
def health_check():
    """
    Basic health check endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: Service is healthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: "healthy"
            timestamp:
              type: string
              example: "2024-01-15T10:30:00Z"
            service:
              type: string
              example: "University Department Chatbot API"
            version:
              type: string
              example: "1.0.0"
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "University Department Chatbot API",
        "version": "1.0.0"
    }), 200


@bp.route('/status', methods=['GET'])
def detailed_status():
    """
    Detailed system status endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: Detailed system status
        schema:
          type: object
          properties:
            status:
              type: string
              example: "operational"
            timestamp:
              type: string
              example: "2024-01-15T10:30:00Z"
            service:
              type: string
              example: "University Department Chatbot API"
            version:
              type: string
              example: "1.0.0"
            system:
              type: object
              properties:
                platform:
                  type: string
                  example: "Linux"
                python_version:
                  type: string
                  example: "3.12.0"
                cpu_percent:
                  type: number
                  example: 15.5
                memory_percent:
                  type: number
                  example: 45.2
            database:
              type: object
              properties:
                status:
                  type: string
                  example: "connected"
            llm_engine:
              type: object
              properties:
                status:
                  type: string
                  example: "ready"
                provider:
                  type: string
                  example: "openai"
    """
    try:
        # Check database connection
        db_status = "connected"
        try:
            db.session.execute('SELECT 1')
        except Exception as e:
            db_status = f"error: {str(e)}"
            logger.warning(f"Database connection check failed: {e}")
        
        # Check LLM engine status
        llm_status = "ready"
        llm_provider = "unknown"
        try:
            llm_engine = create_llm_engine(current_app)
            llm_provider = llm_engine.provider.model if hasattr(llm_engine, 'provider') else "unknown"
        except Exception as e:
            llm_status = f"error: {str(e)}"
            logger.warning(f"LLM engine check failed: {e}")
        
        # Get system information
        system_info = {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent
        }
        
        return jsonify({
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": "University Department Chatbot API",
            "version": "1.0.0",
            "system": system_info,
            "database": {
                "status": db_status
            },
            "llm_engine": {
                "status": llm_status,
                "provider": llm_provider
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in detailed status check: {str(e)}")
        return jsonify({
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": "University Department Chatbot API",
            "version": "1.0.0",
            "error": str(e)
        }), 500


@bp.route('/ping', methods=['GET'])
def ping():
    """
    Simple ping endpoint for load balancer health checks
    ---
    tags:
      - Health
    responses:
      200:
        description: Pong response
        schema:
          type: object
          properties:
            pong:
              type: string
              example: "pong"
            timestamp:
              type: string
              example: "2024-01-15T10:30:00Z"
    """
    return jsonify({
        "pong": "pong",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200
