"""
API Version 1 package.

Exposes the v1 blueprint `bp` and registers routes under it.
"""

from flask import Blueprint

# Public blueprint for v1
bp = Blueprint("api_v1", __name__)

# Import routes to register them with the blueprint
from app.api.routes.v1 import chat_routes, health_routes  # noqa: E402,F401

__all__ = ["bp"]


