"""
Chat Service

This service handles chat session logic and message processing.
"""

import uuid
from typing import List, Dict, Optional
from datetime import datetime
from app.core import LLMEngine
from app.database import db
from app.models import ChatSession, ChatMessage, User
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """Service for handling chat operations"""
    
    def __init__(self, llm_engine: LLMEngine):
        """
        Initialize chat service.
        
        Args:
            llm_engine: LLM engine instance
        """
        self.llm_engine = llm_engine
    
    def create_session(self, user_id: Optional[int] = None, title: Optional[str] = None) -> ChatSession:
        """
        Create a new chat session.
        
        Args:
            user_id: Optional user ID
            title: Optional session title
            
        Returns:
            Created chat session
        """
        session = ChatSession(
            user_id=user_id,
            session_id=str(uuid.uuid4()),
            title=title or f"Chat Session {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        )
        
        db.session.add(session)
        db.session.commit()
        
        logger.info(f"Created chat session: {session.session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Get chat session by session ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Chat session or None
        """
        return ChatSession.query.filter_by(session_id=session_id).first()
    
    def send_message(
        self,
        session_id: str,
        user_message: str,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict:
        """
        Send a message and get response.
        
        Args:
            session_id: Chat session ID
            user_message: User's message
            system_message: Optional system message
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Response dictionary with message and metadata
        """
        # Get or create session
        session = self.get_session(session_id)
        if not session:
            session = self.create_session()
            session_id = session.session_id
        
        # Save user message
        user_msg = ChatMessage(
            session_id=session.id,
            role='user',
            content=user_message
        )
        db.session.add(user_msg)
        
        # Get conversation history
        conversation_history = self._get_conversation_history(session.id)
        
        try:
            # Generate response
            response_text = self.llm_engine.chat(
                user_message=user_message,
                system_message=system_message,
                conversation_history=conversation_history,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Save assistant message
            assistant_msg = ChatMessage(
                session_id=session.id,
                role='assistant',
                content=response_text,
                model_used=self.llm_engine.provider.model
            )
            db.session.add(assistant_msg)
            db.session.commit()
            
            logger.info(f"Generated response for session {session_id}")
            
            return {
                "response": response_text,
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "model": self.llm_engine.provider.model
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error generating response for session {session_id}: {str(e)}")
            raise
    
    def _get_conversation_history(self, session_db_id: int, limit: int = 10) -> List[Dict[str, str]]:
        """
        Get conversation history for a session.
        
        Args:
            session_db_id: Database ID of the session
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message dictionaries
        """
        messages = ChatMessage.query.filter_by(session_id=session_db_id)\
            .order_by(ChatMessage.created_at.desc())\
            .limit(limit * 2)\
            .all()
        
        # Reverse to get chronological order
        messages.reverse()
        
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
    
    def get_session_messages(self, session_id: str, limit: int = 50) -> List[Dict]:
        """
        Get messages for a session.
        
        Args:
            session_id: Session ID
            limit: Maximum number of messages
            
        Returns:
            List of message dictionaries
        """
        session = self.get_session(session_id)
        if not session:
            return []
        
        messages = ChatMessage.query.filter_by(session_id=session.id)\
            .order_by(ChatMessage.created_at.asc())\
            .limit(limit)\
            .all()
        
        return [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
                "model_used": msg.model_used
            }
            for msg in messages
        ]
