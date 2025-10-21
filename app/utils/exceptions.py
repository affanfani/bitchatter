"""
Custom Exceptions

This module contains custom exception classes for the application.
"""


class APIException(Exception):
    """Base API exception"""
    
    def __init__(self, message: str, status_code: int = 400, details: str = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class ValidationError(APIException):
    """Validation error exception"""
    
    def __init__(self, message: str = "Validation error", details: str = None):
        super().__init__(message, 400, details)


class NotFoundError(APIException):
    """Not found error exception"""
    
    def __init__(self, message: str = "Resource not found", details: str = None):
        super().__init__(message, 404, details)


class LLMError(APIException):
    """LLM service error exception"""
    
    def __init__(self, message: str = "LLM service error", details: str = None):
        super().__init__(message, 500, details)


class RateLimitError(APIException):
    """Rate limit exceeded exception"""
    
    def __init__(self, message: str = "Rate limit exceeded", details: str = None):
        super().__init__(message, 429, details)
