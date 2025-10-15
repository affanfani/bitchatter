"""
Application Entry Point

This is the main entry point for running the Flask application.
It creates the Flask app instance and runs the development server.
"""

from flask import Flask
from config.swagger_config import init_swagger

# Create Flask application
app = Flask(__name__)

# Initialize Swagger documentation
swagger = init_swagger(app)

# Simple test route
@app.route('/')
def index():
    return {
        "message": "Welcome to University Department Chatbot API",
        "docs": "Visit /apidocs for API documentation"
    }

if __name__ == '__main__':
    print("Starting Flask application with Swagger documentation...")
    print("API Documentation available at: http://localhost:5000/apidocs")
    app.run(debug=True, host='0.0.0.0', port=5000)
