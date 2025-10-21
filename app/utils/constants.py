"""
Application Constants

This module contains application-wide constants.
"""

# API Constants
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Chat Constants
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000
MAX_MESSAGE_LENGTH = 4000
MAX_CONVERSATION_HISTORY = 20

# Rate Limiting
DEFAULT_RATE_LIMIT = 60  # requests per minute

# Model Constants
DEFAULT_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Response Messages
MESSAGES = {
    "WELCOME": "Welcome to University Department Chatbot API",
    "INVALID_REQUEST": "Invalid request data",
    "MESSAGE_REQUIRED": "Message is required",
    "SESSION_NOT_FOUND": "Chat session not found",
    "LLM_ERROR": "Failed to generate response",
    "RATE_LIMIT_EXCEEDED": "Rate limit exceeded"
}
