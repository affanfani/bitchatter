"""
Application Entry Point

This is the main entry point for running the Flask application.
It creates the Flask app instance and runs the development server.
"""

import os
import logging
from app.main import create_app

# Create app instance
app = create_app()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("Starting University Department Chatbot API")
    logger.info("Docs available at /apidocs")
    logger.info("Current model: %s", app.config['OPENROUTER_MODEL'])
    app.run(debug=True, host='0.0.0.0', port=5000)