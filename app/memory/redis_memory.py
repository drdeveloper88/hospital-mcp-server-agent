"""
Redis-based memory management for multi-agent system.
"""
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import aioredis
from app.config import settings

logger = logging.getLogger(__name__)


class RedisMemoryManager:
    """Manages conversation and context memory using Redis."""
    
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None
        self.ttl = settings.CACHE_TTL
        
    async def init(self):
        """Initialize Redis connection."""
        try:
            self.redis = await aioredis.from_url(settings.REDIS_URL)
            await self.redis.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def close(self):
        """Close Redis connection."""
        if self.redis:
            await self.redis.close()
    
    async def save_conversation(
        self, 
        session_id: str, 
        messages: List[Dict[str, Any]]
    ) -> bool:
        """Save conversation history."""
        try:
            key = f"conversation:{session_id}"
            value = json.dumps({
                "messages": messages,
                "timestamp": datetime.utcnow().isoformat()
            })
            await self.redis.setex(key, self.ttl, value)
            return True
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")
            return False
    
    async def get_conversation(self, session_id: str) -> Optional[List[Dict]]:
        """Retrieve conversation history."""
        try:
            key = f"conversation:{session_id}"
            data = await self.redis.get(key)
            if data:
                parsed = json.loads(data)
                return parsed.get("messages", [])
            return []
        except Exception as e:
            logger.error(f"Failed to retrieve conversation: {e}")
            return None
    
    async def save_context(
        self, 
        session_id: str, 
        context: Dict[str, Any]
    ) -> bool:
        """Save agent context."""
        try:
            key = f"context:{session_id}"
            value = json.dumps({
                "context": context,
                "timestamp": datetime.utcnow().isoformat()
            })
            await self.redis.setex(key, self.ttl, value)
            return True
        except Exception as e:
            logger.error(f"Failed to save context: {e}")
            return False
    
    async def get_context(self, session_id: str) -> Optional[Dict]:
        """Retrieve agent context."""
        try:
            key = f"context:{session_id}"
            data = await self.redis.get(key)
            if data:
                parsed = json.loads(data)
                return parsed.get("context", {})
            return {}
        except Exception as e:
            logger.error(f"Failed to retrieve context: {e}")
            return None

memory_manager = RedisMemoryManager()
