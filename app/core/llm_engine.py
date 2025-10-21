"""
LLM Engine

This module provides a unified interface for interacting with various LLM providers
including OpenRouter, OpenAI, Anthropic, etc.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate a response from the LLM"""
        pass


class OpenRouterProvider(LLMProvider):
    """OpenRouter LLM provider implementation"""
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://openrouter.ai/api/v1",
        model: str = "meta-llama/llama-3.3-70b-instruct:free",
        site_url: Optional[str] = None,
        site_name: Optional[str] = None
    ):
        """
        Initialize OpenRouter provider.
        
        Args:
            api_key: OpenRouter API key
            base_url: OpenRouter base URL
            model: Model identifier
            site_url: Optional site URL for rankings
            site_name: Optional site name for rankings
        """
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model = model
        self.site_url = site_url
        self.site_name = site_name
    
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate a response from OpenRouter LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters
            
        Returns:
            Generated text response
        """
        try:
            extra_headers = {}
            if self.site_url:
                extra_headers["HTTP-Referer"] = self.site_url
            if self.site_name:
                extra_headers["X-Title"] = self.site_name
            
            completion_params = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "extra_body": {}
            }
            
            if max_tokens:
                completion_params["max_tokens"] = max_tokens
            
            if extra_headers:
                completion_params["extra_headers"] = extra_headers
            
            completion = self.client.chat.completions.create(**completion_params)
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenRouter API error: {str(e)}")
            raise


class LLMEngine:
    """Main LLM engine that manages different providers"""
    
    def __init__(self, provider: LLMProvider):
        """
        Initialize LLM engine with a provider.
        
        Args:
            provider: LLM provider instance
        """
        self.provider = provider
    
    def chat(
        self,
        user_message: str,
        system_message: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Simplified chat interface.
        
        Args:
            user_message: User's message
            system_message: Optional system message for context
            conversation_history: Optional list of previous messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters
            
        Returns:
            Assistant's response
        """
        messages = []
        
        # Add system message if provided
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return self.provider.generate_response(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters
            
        Returns:
            Generated text response
        """
        return self.provider.generate_response(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )


def create_llm_engine(app) -> LLMEngine:
    """
    Factory function to create LLM engine from Flask app config.
    
    Args:
        app: Flask application instance
        
    Returns:
        Configured LLMEngine instance
    """
    provider = OpenRouterProvider(
        api_key=app.config['OPENROUTER_API_KEY'],
        base_url=app.config['OPENROUTER_BASE_URL'],
        model=app.config['OPENROUTER_MODEL'],
        site_url=app.config.get('SITE_URL'),
        site_name=app.config.get('SITE_NAME')
    )
    
    return LLMEngine(provider)
