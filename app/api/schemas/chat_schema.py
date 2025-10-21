"""
Chat API Schemas

This module contains Pydantic-like schemas for chat API validation.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class ChatMessageRequest:
    """Schema for chat message request"""
    message: str
    session_id: Optional[str] = None
    system_message: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    
    def validate(self) -> Dict[str, Any]:
        """Validate the request data"""
        errors = {}
        
        if not self.message or not self.message.strip():
            errors['message'] = 'Message is required and cannot be empty'
        
        if self.temperature < 0 or self.temperature > 2:
            errors['temperature'] = 'Temperature must be between 0 and 2'
        
        if self.max_tokens is not None and self.max_tokens <= 0:
            errors['max_tokens'] = 'Max tokens must be a positive integer'
        
        return errors


@dataclass
class ChatMessageResponse:
    """Schema for chat message response"""
    response: str
    session_id: str
    timestamp: str
    model: str
    message_id: Optional[str] = None


@dataclass
class ChatSessionResponse:
    """Schema for chat session response"""
    session_id: str
    title: str
    created_at: str
    message_count: int
    is_active: bool


@dataclass
class ChatHistoryResponse:
    """Schema for chat history response"""
    session_id: str
    messages: List[Dict[str, Any]]
    total_count: int
