"""
Intent Matching API Routes

This module contains API endpoints for intent matching using the vector database.
"""

from flask import request, jsonify, current_app
from app.api.v1 import bp
from app.services.intent_matcher import create_intent_matcher
from app.utils.exceptions import APIException
import logging

logger = logging.getLogger(__name__)


@bp.route('/intent/match', methods=['POST'])
def match_intent():
    """
    Match user query to the most relevant intent
    ---
    tags:
      - Intent Matching
    parameters:
      - in: body
        name: body
        description: Intent matching request
        required: true
        schema:
          type: object
          required:
            - query
          properties:
            query:
              type: string
              description: User's query text
              example: "What courses are available?"
            k:
              type: integer
              description: Number of top matches to return
              default: 1
              example: 1
            threshold:
              type: number
              description: Minimum similarity threshold (0-1)
              default: 0.5
              example: 0.5
    responses:
      200:
        description: Matched intent
        schema:
          type: object
          properties:
            query:
              type: string
              example: "What courses are available?"
            matched:
              type: boolean
              example: true
            intent:
              type: object
              properties:
                tag:
                  type: string
                  example: "course_inquiry"
                pattern:
                  type: string
                  example: "What courses do you offer?"
                responses:
                  type: array
                  items:
                    type: string
                  example: ["We offer courses in Computer Science, Engineering, and more."]
                score:
                  type: number
                  example: 0.87
                rank:
                  type: integer
                  example: 1
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            raise APIException("Query is required", status_code=400)
        
        query = data.get('query', '').strip()
        if not query:
            raise APIException("Query cannot be empty", status_code=400)
        
        k = data.get('k', 1)
        threshold = data.get('threshold', 0.5)
        
        # Create intent matcher (will use pre-loaded vector DB)
        intent_matcher = create_intent_matcher(current_app)
        
        if not intent_matcher.is_loaded():
            raise APIException(
                "Vector database not available. Please ensure data is loaded.",
                status_code=503
            )
        
        # Set custom threshold if provided
        if threshold != intent_matcher.threshold:
            intent_matcher.threshold = threshold
        
        # Match intent
        result = intent_matcher.match_intent(query, k=k)
        
        if result:
            return jsonify({
                "query": query,
                "matched": True,
                "intent": {
                    "tag": result['metadata']['tag'],
                    "pattern": result['metadata']['pattern'],
                    "responses": result['metadata'].get('responses', []),
                    "score": result['score'],
                    "rank": result['rank']
                }
            }), 200
        else:
            return jsonify({
                "query": query,
                "matched": False,
                "message": f"No intent matched above threshold {threshold}"
            }), 200
        
    except APIException as e:
        logger.warning(f"API exception in match_intent: {e.message}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in match_intent: {str(e)}")
        raise APIException("Internal server error", status_code=500)


@bp.route('/intent/search', methods=['POST'])
def search_intents():
    """
    Search for multiple matching intents
    ---
    tags:
      - Intent Matching
    parameters:
      - in: body
        name: body
        description: Intent search request
        required: true
        schema:
          type: object
          required:
            - query
          properties:
            query:
              type: string
              description: User's query text
              example: "admission requirements"
            k:
              type: integer
              description: Number of results to return
              default: 5
              example: 5
            min_score:
              type: number
              description: Minimum similarity score filter
              example: 0.3
    responses:
      200:
        description: Search results
        schema:
          type: object
          properties:
            query:
              type: string
              example: "admission requirements"
            total_results:
              type: integer
              example: 5
            results:
              type: array
              items:
                type: object
                properties:
                  tag:
                    type: string
                    example: "admission_info"
                  pattern:
                    type: string
                    example: "What are the admission requirements?"
                  score:
                    type: number
                    example: 0.85
                  rank:
                    type: integer
                    example: 1
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            raise APIException("Query is required", status_code=400)
        
        query = data.get('query', '').strip()
        if not query:
            raise APIException("Query cannot be empty", status_code=400)
        
        k = data.get('k', 5)
        min_score = data.get('min_score')
        
        # Create intent matcher
        intent_matcher = create_intent_matcher(current_app)
        
        if not intent_matcher.is_loaded():
            raise APIException(
                "Vector database not available. Please ensure data is loaded.",
                status_code=503
            )
        
        # Search intents
        results = intent_matcher.search_intents(query, k=k, min_score=min_score)
        
        # Format results
        formatted_results = [
            {
                "tag": r['metadata']['tag'],
                "pattern": r['metadata']['pattern'],
                "score": r['score'],
                "rank": r['rank']
            }
            for r in results
        ]
        
        return jsonify({
            "query": query,
            "total_results": len(formatted_results),
            "results": formatted_results
        }), 200
        
    except APIException as e:
        logger.warning(f"API exception in search_intents: {e.message}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in search_intents: {str(e)}")
        raise APIException("Internal server error", status_code=500)


@bp.route('/intent/response', methods=['POST'])
def get_intent_response():
    """
    Get a direct response for a user query based on matched intent
    ---
    tags:
      - Intent Matching
    parameters:
      - in: body
        name: body
        description: Intent response request
        required: true
        schema:
          type: object
          required:
            - query
          properties:
            query:
              type: string
              description: User's query text
              example: "Hello"
            randomize:
              type: boolean
              description: Randomly select from multiple responses
              default: true
              example: true
    responses:
      200:
        description: Intent-based response
        schema:
          type: object
          properties:
            query:
              type: string
              example: "Hello"
            response:
              type: string
              example: "Hi there! How can I assist you?"
            intent_tag:
              type: string
              example: "greeting"
            matched:
              type: boolean
              example: true
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            raise APIException("Query is required", status_code=400)
        
        query = data.get('query', '').strip()
        if not query:
            raise APIException("Query cannot be empty", status_code=400)
        
        randomize = data.get('randomize', True)
        
        # Create intent matcher
        intent_matcher = create_intent_matcher(current_app)
        
        if not intent_matcher.is_loaded():
            raise APIException(
                "Vector database not available. Please ensure data is loaded.",
                status_code=503
            )
        
        # Get response
        response = intent_matcher.get_response(query, randomize=randomize)
        intent_tag = intent_matcher.get_intent_tag(query)
        
        return jsonify({
            "query": query,
            "response": response,
            "intent_tag": intent_tag,
            "matched": intent_tag is not None
        }), 200
        
    except APIException as e:
        logger.warning(f"API exception in get_intent_response: {e.message}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_intent_response: {str(e)}")
        raise APIException("Internal server error", status_code=500)


@bp.route('/intent/stats', methods=['GET'])
def get_vector_db_stats():
    """
    Get vector database statistics
    ---
    tags:
      - Intent Matching
    responses:
      200:
        description: Vector database statistics
        schema:
          type: object
          properties:
            loaded:
              type: boolean
              example: true
            total_vectors:
              type: integer
              example: 2663
            dimension:
              type: integer
              example: 384
            model_name:
              type: string
              example: "all-MiniLM-L6-v2"
            threshold:
              type: number
              example: 0.5
      500:
        description: Internal server error
    """
    try:
        # Create intent matcher
        intent_matcher = create_intent_matcher(current_app)
        
        # Get stats
        stats = intent_matcher.get_stats()
        
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in get_vector_db_stats: {str(e)}")
        raise APIException("Internal server error", status_code=500)

