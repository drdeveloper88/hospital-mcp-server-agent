"""
Streaming chat implementation for real-time responses.
"""
import logging
import asyncio
from typing import AsyncGenerator, Dict, Any
from fastapi import HTTPException
from app.llm.ollama_client import ollama_client
from app.memory.redis_memory import memory_manager
from app.agents.supervisor import supervisor, AgentState

logger = logging.getLogger(__name__)


class StreamingChatService:
    """Service for streaming chat responses."""
    
    async def stream_response(
        self,
        session_id: str,
        message: str,
        system_prompt: str = None
    ) -> AsyncGenerator[str, None]:
        """Stream chat response."""
        try:
            # Retrieve conversation history
            history = await memory_manager.get_conversation(session_id)
            
            # Build prompt with context
            context = {
                "session_id": session_id,
                "message": message,
                "history_length": len(history) if history else 0
            }
            
            # Create agent state
            state = AgentState(
                messages=history or [],
                context=context,
                current_agent="supervisor",
                task=message
            )
            
            # Add user message
            state.messages.append({"role": "user", "content": message})
            
            # Process through supervisor
            async for chunk in ollama_client.generate(
                message,
                system=system_prompt,
                stream=True
            ):
                yield chunk
                await asyncio.sleep(0.01)  # Prevent blocking
            
            # Save updated conversation
            await memory_manager.save_conversation(session_id, state.messages)
            
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"Error: {str(e)}"
    
    async def get_response(
        self,
        session_id: str,
        message: str,
        system_prompt: str = None
    ) -> Dict[str, Any]:
        """Get non-streaming response."""
        try:
            history = await memory_manager.get_conversation(session_id)
            
            context = {
                "session_id": session_id,
                "message": message,
                "history_length": len(history) if history else 0
            }
            
            state = AgentState(
                messages=history or [],
                context=context,
                current_agent="supervisor",
                task=message
            )
            
            state.messages.append({"role": "user", "content": message})
            
            response = await ollama_client.generate(
                message,
                system=system_prompt,
                stream=False
            )
            
            state.messages.append({"role": "assistant", "content": response})
            
            await memory_manager.save_conversation(session_id, state.messages)
            
            return {
                "response": response,
                "session_id": session_id,
                "messages_count": len(state.messages)
            }
        except Exception as e:
            logger.error(f"Response error: {e}")
            raise

chat_service = StreamingChatService()
