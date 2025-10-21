"""
Utility Helpers

This module contains helper functions for the application.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional


def generate_session_id() -> str:
    """Generate a unique session ID"""
    return str(uuid.uuid4())


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format datetime as ISO string"""
    if dt is None:
        dt = datetime.utcnow()
    return dt.isoformat() + "Z"


def create_response(data: Any, status_code: int = 200, message: Optional[str] = None) -> Dict:
    """Create a standardized API response"""
    response = {
        "data": data,
        "timestamp": format_timestamp(),
        "status_code": status_code
    }
    
    if message:
        response["message"] = message
    
    return response


def create_error_response(error: str, status_code: int = 400, details: Optional[str] = None) -> Dict:
    """Create a standardized error response"""
    response = {
        "error": error,
        "timestamp": format_timestamp(),
        "status_code": status_code
    }
    
    if details:
        response["details"] = details
    
    return response
