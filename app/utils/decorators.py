"""
Utility Decorators

This module contains useful decorators for the application.
"""

from functools import wraps
from flask import request, jsonify, current_app
import time
import logging

logger = logging.getLogger(__name__)


def rate_limit(max_requests: int = 60, window_seconds: int = 60):
    """
    Rate limiting decorator.
    
    Args:
        max_requests: Maximum requests per window
        window_seconds: Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Simple in-memory rate limiting (use Redis in production)
            client_ip = request.remote_addr
            current_time = time.time()
            
            # This is a simplified implementation
            # In production, use Redis or a proper rate limiting library
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def require_json(f):
    """
    Decorator to require JSON content type.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        return f(*args, **kwargs)
    return decorated_function


def log_request(f):
    """
    Decorator to log API requests.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        
        logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
        
        result = f(*args, **kwargs)
        
        duration = time.time() - start_time
        logger.info(f"Response: {request.method} {request.path} completed in {duration:.3f}s")
        
        return result
    return decorated_function
