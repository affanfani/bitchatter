"""
Web Routes

This module contains routes for serving web pages and handling web requests.
"""

from flask import render_template, request, jsonify, current_app
from app.web import web_bp
from app.services.rag_service import RAGService
from app.core.llm_engine import create_llm_engine
import logging

logger = logging.getLogger(__name__)


def get_rag_service():
    """Get RAG service instance"""
    llm_engine = create_llm_engine(current_app)
    vector_db = current_app.config.get('VECTOR_DB')
    return RAGService(llm_engine, vector_db)


@web_bp.route('/')
def index():
    """
    Serve the main chatbot interface.
    
    Returns:
        Rendered HTML template
    """
    return render_template('index.html')


@web_bp.route('/get_response', methods=['POST'])
def get_response():
    """
    Handle chat requests from the web interface.
    
    Expected JSON payload:
    {
        "user_input": "User's message"
    }
    
    Returns:
        JSON response with the bot's answer
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'response': 'Error: No data received. Please try again.'
            }), 400
        
        user_input = data.get('user_input', '').strip()
        if not user_input:
            return jsonify({
                'response': 'Error: Please enter a message.'
            }), 400
        
        # Get RAG service and generate response
        rag_service = get_rag_service()
        response = rag_service.generate_response(user_input)
        
        logger.info(f"User query: {user_input[:50]}... | Response generated successfully")
        
        return jsonify({
            'response': response
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_response: {str(e)}", exc_info=True)
        return jsonify({
            'response': 'I apologize, but I encountered an error processing your request. Please try again or rephrase your question.'
        }), 500


@web_bp.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint for web service.
    
    Returns:
        JSON response with service status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'web'
    }), 200

