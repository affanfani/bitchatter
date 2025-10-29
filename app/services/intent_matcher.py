"""
Intent Matcher Service

This module provides intent matching capabilities using the FAISS vector database.
"""

import logging
import random
from typing import Dict, Any, Optional, List
from pathlib import Path

from app.utils.vector_db import FAISSVectorDB

logger = logging.getLogger(__name__)


class IntentMatcher:
    """Service for matching user queries to intents using vector similarity"""
    
    def __init__(
        self,
        vector_db: Optional[FAISSVectorDB] = None,
        vector_db_path: str = 'data/vector_db',
        threshold: float = 0.5,
        auto_load: bool = True
    ):
        """
        Initialize Intent Matcher.
        
        Args:
            vector_db: Pre-loaded FAISSVectorDB instance (optional)
            vector_db_path: Path to vector database directory
            threshold: Minimum similarity score for matching (0-1)
            auto_load: Whether to automatically load the database
        """
        self.vector_db_path = vector_db_path
        self.threshold = threshold
        self.vector_db = vector_db
        self._loaded = vector_db is not None
        
        # If vector_db is provided, no need to load
        if self.vector_db is None and auto_load:
            self.load()
    
    def load(self):
        """Load the vector database"""
        try:
            logger.info(f"Loading vector database from {self.vector_db_path}")
            
            index_path = f'{self.vector_db_path}/faiss.index'
            metadata_path = f'{self.vector_db_path}/metadata.pkl'
            config_path = f'{self.vector_db_path}/config.json'
            
            # Check if files exist
            if not Path(index_path).exists():
                logger.error(f"FAISS index not found at {index_path}")
                logger.error("Please run 'python build_vector_db.py' to create the index")
                return False
            
            self.vector_db = FAISSVectorDB()
            self.vector_db.load(index_path, metadata_path, config_path)
            
            stats = self.vector_db.get_stats()
            logger.info(f"Vector database loaded: {stats['total_vectors']} vectors")
            self._loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Error loading vector database: {e}", exc_info=True)
            self._loaded = False
            return False
    
    def is_loaded(self) -> bool:
        """Check if the vector database is loaded"""
        return self._loaded and self.vector_db is not None
    
    def match_intent(
        self,
        user_query: str,
        k: int = 5,
        return_all: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Match user query to the best intent.
        
        Args:
            user_query: User's input text
            k: Number of candidates to retrieve
            return_all: Whether to return all candidates or just the best match
            
        Returns:
            Intent metadata with score, or None if no match above threshold
        """
        if not self.is_loaded():
            logger.warning("Vector database not loaded")
            return None
        
        try:
            results = self.vector_db.search(user_query, k=k)
            
            if not results:
                return None
            
            if return_all:
                # Return all results above threshold
                filtered = [r for r in results if r['score'] >= self.threshold]
                return filtered if filtered else None
            
            # Return best match if above threshold
            best_match = results[0]
            if best_match['score'] >= self.threshold:
                return best_match
            
            return None
            
        except Exception as e:
            logger.error(f"Error matching intent: {e}", exc_info=True)
            return None
    
    def get_response(
        self,
        user_query: str,
        randomize: bool = True,
        fallback: str = "I'm not sure how to help with that. Can you rephrase?"
    ) -> str:
        """
        Get a response for a user query.
        
        Args:
            user_query: User's input text
            randomize: Whether to randomly select from multiple responses
            fallback: Fallback message if no intent matches
            
        Returns:
            Response string
        """
        intent = self.match_intent(user_query)
        
        if intent and intent['metadata'].get('responses'):
            responses = intent['metadata']['responses']
            
            if randomize and len(responses) > 1:
                return random.choice(responses)
            
            return responses[0]
        
        return fallback
    
    def get_intent_tag(self, user_query: str) -> Optional[str]:
        """
        Get the intent tag for a user query.
        
        Args:
            user_query: User's input text
            
        Returns:
            Intent tag string or None
        """
        intent = self.match_intent(user_query)
        
        if intent:
            return intent['metadata'].get('tag')
        
        return None
    
    def search_intents(
        self,
        user_query: str,
        k: int = 10,
        min_score: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for multiple matching intents.
        
        Args:
            user_query: User's input text
            k: Number of results to return
            min_score: Optional minimum score threshold
            
        Returns:
            List of matching intents with scores
        """
        if not self.is_loaded():
            logger.warning("Vector database not loaded")
            return []
        
        try:
            results = self.vector_db.search(user_query, k=k)
            
            if min_score is not None:
                results = [r for r in results if r['score'] >= min_score]
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching intents: {e}", exc_info=True)
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get vector database statistics.
        
        Returns:
            Dictionary with statistics
        """
        if not self.is_loaded():
            return {
                'loaded': False,
                'error': 'Vector database not loaded'
            }
        
        stats = self.vector_db.get_stats()
        stats['loaded'] = True
        stats['threshold'] = self.threshold
        stats['path'] = self.vector_db_path
        
        return stats


def create_intent_matcher(app=None, **kwargs) -> IntentMatcher:
    """
    Factory function to create IntentMatcher from Flask app config.
    
    Args:
        app: Optional Flask application instance
        **kwargs: Additional arguments to pass to IntentMatcher
        
    Returns:
        Configured IntentMatcher instance
    """
    if app is not None:
        # Check if vector_db is already loaded in app config
        vector_db = app.config.get('VECTOR_DB')
        vector_db_path = app.config.get('VECTOR_DB_PATH', 'data/vector_db')
        threshold = app.config.get('INTENT_MATCH_THRESHOLD', 0.5)
        
        # If vector_db is already loaded, use it
        if vector_db is not None:
            logger.info("Using pre-loaded vector database from app config")
            return IntentMatcher(
                vector_db=vector_db,
                vector_db_path=vector_db_path,
                threshold=threshold,
                auto_load=False,  # Don't load again
                **kwargs
            )
        
        return IntentMatcher(
            vector_db_path=vector_db_path,
            threshold=threshold,
            **kwargs
        )
    
    return IntentMatcher(**kwargs)

