"""
Database-based memory for persistent conversation storage.
"""
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base

logger = logging.getLogger(__name__)


class ConversationMemory(Base):
    """Database model for conversation memory."""
    __tablename__ = "conversation_memory"
    
    session_id = Column(String(255), primary_key=True)
    messages = Column(Text)
    context = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DatabaseMemoryManager:
    """Manages memory using PostgreSQL database."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def save_conversation(
        self, 
        session_id: str, 
        messages: List[Dict[str, Any]]
    ) -> bool:
        """Save conversation to database."""
        try:
            memory = ConversationMemory(
                session_id=session_id,
                messages=json.dumps(messages)
            )
            self.db.merge(memory)
            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")
            await self.db.rollback()
            return False
    
    async def get_conversation(self, session_id: str) -> Optional[List[Dict]]:
        """Retrieve conversation from database."""
        try:
            stmt = select(ConversationMemory).where(
                ConversationMemory.session_id == session_id
            )
            result = await self.db.execute(stmt)
            memory = result.scalar_one_or_none()
            if memory:
                return json.loads(memory.messages)
            return []
        except Exception as e:
            logger.error(f"Failed to retrieve conversation: {e}")
            return None
