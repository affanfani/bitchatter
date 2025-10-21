"""
Database Models

This module contains SQLAlchemy models for the application.
"""

from datetime import datetime
from app.database import db


class BaseModel(db.Model):
    """Base model with common fields"""
    
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(BaseModel):
    """User model"""
    
    __tablename__ = 'users'
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    chat_sessions = db.relationship('ChatSession', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class ChatSession(BaseModel):
    """Chat session model"""
    
    __tablename__ = 'chat_sessions'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_id = db.Column(db.String(36), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ChatSession {self.session_id}>'


class ChatMessage(BaseModel):
    """Chat message model"""
    
    __tablename__ = 'chat_messages'
    
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = db.Column(db.Text, nullable=False)
    model_used = db.Column(db.String(100), nullable=True)
    tokens_used = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return f'<ChatMessage {self.role}: {self.content[:50]}...>'