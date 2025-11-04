"""
RAG (Retrieval-Augmented Generation) Service

This service combines vector database retrieval with LLM generation
to provide accurate, context-aware responses.
"""

from typing import List, Dict, Optional, Any
from app.core.llm_engine import LLMEngine
from app.utils.vector_db import FAISSVectorDB
import logging

logger = logging.getLogger(__name__)


class RAGService:
    """Service for Retrieval-Augmented Generation"""
    
    # Professional system prompt for formal responses
    SYSTEM_PROMPT = """You are BIT Chatter, a professional and knowledgeable virtual assistant for the Institute of Business and Information Technology (IBIT) at Punjab University Lahore.

Your role is to:
1. Provide accurate, professional, and formal responses to queries about IBIT
2. Use the provided context information to answer questions accurately
3. Be helpful, courteous, and informative
4. Maintain a professional tone at all times
5. If you don't have specific information in the context, politely acknowledge this and provide general guidance

Guidelines:
- Always be respectful and professional
- Provide clear, well-structured answers
- Use proper grammar and formal language
- If the context doesn't contain relevant information, say so honestly
- Stay focused on IBIT-related topics
- Be concise but comprehensive

Context Information:
{context}

Based on the above context, please provide a professional and accurate response to the user's query."""
    
    def __init__(
        self,
        llm_engine: LLMEngine,
        vector_db: Optional[FAISSVectorDB] = None,
        top_k: int = 5,
        similarity_threshold: float = 0.3
    ):
        """
        Initialize RAG service.
        
        Args:
            llm_engine: LLM engine instance
            vector_db: Vector database for semantic search
            top_k: Number of top results to retrieve
            similarity_threshold: Minimum similarity score for results
        """
        self.llm_engine = llm_engine
        self.vector_db = vector_db
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
    
    def retrieve_context(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from vector database.
        
        Args:
            query: User query
            
        Returns:
            List of relevant context items with metadata
        """
        if not self.vector_db:
            logger.warning("Vector database not available")
            return []
        
        try:
            results = self.vector_db.search(query, k=self.top_k, return_scores=True)
            
            # Filter by similarity threshold
            filtered_results = [
                result for result in results
                if result.get('score', 0) >= self.similarity_threshold
            ]
            
            logger.info(f"Retrieved {len(filtered_results)} relevant contexts for query: {query[:50]}...")
            return filtered_results
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}", exc_info=True)
            return []
    
    def format_context(self, results: List[Dict[str, Any]]) -> str:
        """
        Format retrieved results into a context string.
        
        Args:
            results: List of search results
            
        Returns:
            Formatted context string
        """
        if not results:
            return "No specific information found in the knowledge base for this query."
        
        context_parts = []
        seen_responses = set()  # To avoid duplicate responses
        
        for i, result in enumerate(results, 1):
            metadata = result.get('metadata', {})
            tag = metadata.get('tag', 'Unknown')
            pattern = metadata.get('pattern', '')
            responses = metadata.get('responses', [])
            score = result.get('score', 0)
            
            # Get unique responses
            unique_responses = [r for r in responses if r not in seen_responses]
            if unique_responses:
                context_parts.append(f"\n[Context {i}] (Relevance: {score:.2f})")
                context_parts.append(f"Topic: {tag}")
                if pattern:
                    context_parts.append(f"Related Query: {pattern}")
                context_parts.append(f"Information: {unique_responses[0]}")
                seen_responses.update(unique_responses)
        
        return "\n".join(context_parts) if context_parts else "No specific information found."
    
    def generate_response(
        self,
        query: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = 500
    ) -> str:
        """
        Generate a response using RAG approach.
        
        Args:
            query: User query
            conversation_history: Optional conversation history
            temperature: LLM temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated response
        """
        try:
            # Step 1: Retrieve relevant context
            context_results = self.retrieve_context(query)
            
            # Step 2: Format context
            context_str = self.format_context(context_results)
            
            # Step 3: Create system message with context
            system_message = self.SYSTEM_PROMPT.format(context=context_str)
            
            # Step 4: Generate response using LLM
            logger.info(f"Generating response with {len(context_results)} context items")
            
            response = self.llm_engine.chat(
                user_message=query,
                system_message=system_message,
                conversation_history=conversation_history,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating RAG response: {str(e)}", exc_info=True)
            return self._get_fallback_response(query, context_results)
    
    def _get_fallback_response(
        self,
        query: str,
        context_results: List[Dict[str, Any]]
    ) -> str:
        """
        Get fallback response if LLM generation fails.
        
        Args:
            query: User query
            context_results: Retrieved context results
            
        Returns:
            Fallback response
        """
        if not context_results:
            return ("I apologize, but I don't have specific information about your query in my knowledge base. "
                   "Please try rephrasing your question or contact IBIT administration directly for assistance.")
        
        # Return the most relevant response from context
        best_result = context_results[0]
        metadata = best_result.get('metadata', {})
        responses = metadata.get('responses', [])
        
        if responses:
            return responses[0]
        
        return ("I apologize, but I'm unable to generate a response at the moment. "
               "Please try again or contact IBIT administration for assistance.")
    
    def get_direct_match(self, query: str) -> Optional[str]:
        """
        Try to get a direct match from the vector database without LLM.
        Useful for simple queries with exact matches.
        
        Args:
            query: User query
            
        Returns:
            Direct response if found, None otherwise
        """
        if not self.vector_db:
            return None
        
        try:
            results = self.vector_db.search(query, k=1, return_scores=True)
            
            if results and results[0].get('score', 0) >= 0.85:  # High confidence threshold
                metadata = results[0].get('metadata', {})
                responses = metadata.get('responses', [])
                if responses:
                    logger.info(f"Direct match found for query: {query[:50]}...")
                    return responses[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error in direct match: {str(e)}")
            return None

