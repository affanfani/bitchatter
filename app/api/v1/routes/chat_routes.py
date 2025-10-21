"""
Chat API Routes

This module contains all chat-related API endpoints for version 1.
"""

from flask import request, jsonify, current_app
from flasgger import swag_from
from app.api.v1 import bp
from app.services.chat_service import ChatService
from app.core.llm_engine import create_llm_engine
from app.api.schemas.chat_schema import ChatMessageRequest, ChatMessageResponse
from app.utils.exceptions import APIException
import logging

logger = logging.getLogger(__name__)

def get_chat_service():
    """Get chat service instance with properly initialized LLM engine"""
    llm_engine = create_llm_engine(current_app)
    return ChatService(llm_engine)


@bp.route('/chat/message', methods=['POST'])
def send_message():
    """
    Send a chat message and get AI response
    ---
    tags:
      - Chat
    parameters:
      - in: body
        name: body
        description: Chat message request
        required: true
        schema:
          type: object
          required:
            - message
          properties:
            message:
              type: string
              description: User's message
              example: "What courses are available in Computer Science?"
            session_id:
              type: string
              description: Optional session ID for continuing conversation
              example: "123e4567-e89b-12d3-a456-426614174000"
            system_message:
              type: string
              description: Optional system message to set context
              example: "You are a helpful university assistant."
            temperature:
              type: number
              description: Sampling temperature (0-2)
              default: 0.7
              example: 0.7
            max_tokens:
              type: integer
              description: Maximum tokens in response
              example: 1000
    responses:
      200:
        description: Chat response
        schema:
          type: object
          properties:
            response:
              type: string
              example: "Computer Science offers courses in programming, algorithms, data structures, and more."
            session_id:
              type: string
              example: "123e4567-e89b-12d3-a456-426614174000"
            timestamp:
              type: string
              example: "2024-01-15T10:30:00Z"
            model:
              type: string
              example: "gpt-3.5-turbo"
      400:
        description: Bad request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Message is required and cannot be empty"
      500:
        description: Internal server error
    """
    try:
        data = request.get_json()
        if not data:
            raise APIException("Request body is required", status_code=400)
        
        # Create request schema and validate
        chat_request = ChatMessageRequest(
            message=data.get('message', ''),
            session_id=data.get('session_id'),
            system_message=data.get('system_message'),
            temperature=data.get('temperature', 0.7),
            max_tokens=data.get('max_tokens')
        )
        
        # Validate request
        errors = chat_request.validate()
        if errors:
            raise APIException("Validation failed", details=errors, status_code=400)
        
        # Send message and get response
        chat_service = get_chat_service()
        result = chat_service.send_message(
            session_id=chat_request.session_id or '',
            user_message=chat_request.message,
            system_message=chat_request.system_message,
            temperature=chat_request.temperature,
            max_tokens=chat_request.max_tokens
        )
        
        return jsonify(result), 200
        
    except APIException as e:
        logger.warning(f"API exception in send_message: {e.message}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in send_message: {str(e)}")
        raise APIException("Internal server error", status_code=500)


@bp.route('/chat/session/<session_id>', methods=['GET'])
def get_session_messages(session_id):
    """
    Get messages for a specific chat session
    ---
    tags:
      - Chat
    parameters:
      - in: path
        name: session_id
        type: string
        required: true
        description: Chat session ID
        example: "123e4567-e89b-12d3-a456-426614174000"
      - in: query
        name: limit
        type: integer
        required: false
        description: Maximum number of messages to return
        default: 50
        example: 50
    responses:
      200:
        description: Session messages
        schema:
          type: object
          properties:
            session_id:
              type: string
              example: "123e4567-e89b-12d3-a456-426614174000"
            messages:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  role:
                    type: string
                    example: "user"
                  content:
                    type: string
                    example: "Hello, how are you?"
                  created_at:
                    type: string
                    example: "2024-01-15T10:30:00Z"
                  model_used:
                    type: string
                    example: "gpt-3.5-turbo"
            total_count:
              type: integer
              example: 2
      404:
        description: Session not found
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        chat_service = get_chat_service()
        messages = chat_service.get_session_messages(session_id, limit)
        
        return jsonify({
            "session_id": session_id,
            "messages": messages,
            "total_count": len(messages)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting session messages: {str(e)}")
        raise APIException("Internal server error", status_code=500)


@bp.route('/chat/session', methods=['POST'])
def create_session():
    """
    Create a new chat session
    ---
    tags:
      - Chat
    parameters:
      - in: body
        name: body
        description: Session creation request
        required: false
        schema:
          type: object
          properties:
            title:
              type: string
              description: Optional session title
              example: "Course Information Chat"
    responses:
      201:
        description: Session created
        schema:
          type: object
          properties:
            session_id:
              type: string
              example: "123e4567-e89b-12d3-a456-426614174000"
            title:
              type: string
              example: "Course Information Chat"
            created_at:
              type: string
              example: "2024-01-15T10:30:00Z"
            message_count:
              type: integer
              example: 0
            is_active:
              type: boolean
              example: true
    """
    try:
        data = request.get_json() or {}
        title = data.get('title')
        
        chat_service = get_chat_service()
        session = chat_service.create_session(title=title)
        
        return jsonify({
            "session_id": session.session_id,
            "title": session.title,
            "created_at": session.created_at.isoformat() + "Z",
            "message_count": 0,
            "is_active": True
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise APIException("Internal server error", status_code=500)
