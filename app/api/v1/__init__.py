"""
API Version 1 package.

Exposes the v1 blueprint `bp` and registers routes under it.
"""

from flask import Blueprint

# Public blueprint for v1
bp = Blueprint("api_v1", __name__)

# Import routes to register them with the blueprint
from app.api.v1.routes import chat_routes, health_routes, intent_routes  # noqa: E402,F401

__all__ = ["bp"]


