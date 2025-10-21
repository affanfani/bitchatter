"""
Core Package

This package contains core functionality for the application including
LLM engines, embeddings, vector stores, and processing pipelines.
"""

from .llm_engine import LLMEngine, LLMProvider, OpenRouterProvider, create_llm_engine

__all__ = ['LLMEngine', 'LLMProvider', 'OpenRouterProvider', 'create_llm_engine']
