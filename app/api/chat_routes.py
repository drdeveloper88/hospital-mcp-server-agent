"""
API routes for chat and streaming.
"""
import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from app.services.chat_service import chat_service
from app.memory.redis_memory import memory_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """Chat request model."""
    session_id: str
    message: str
    system_prompt: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    session_id: str
    messages_count: int


@router.post("/stream")
async def stream_chat(request: ChatRequest):
    """Stream chat response."""
    try:
        return StreamingResponse(
            chat_service.stream_response(
                request.session_id,
                request.message,
                request.system_prompt
            ),
            media_type="text/event-stream"
        )
    except Exception as e:
        logger.error(f"Stream chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest) -> ChatResponse:
    """Send message and get response."""
    try:
        response = await chat_service.get_response(
            request.session_id,
            request.message,
            request.system_prompt
        )
        return ChatResponse(**response)
    except Exception as e:
        logger.error(f"Send message error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get conversation history."""
    try:
        messages = await memory_manager.get_conversation(session_id)
        return {
            "session_id": session_id,
            "messages": messages,
            "count": len(messages) if messages else 0
        }
    except Exception as e:
        logger.error(f"Get history error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear conversation history."""
    try:
        await memory_manager.save_conversation(session_id, [])
        return {"status": "cleared", "session_id": session_id}
    except Exception as e:
        logger.error(f"Clear history error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
