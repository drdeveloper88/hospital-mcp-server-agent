"""
Health check and status endpoints.
"""
import logging
from fastapi import APIRouter
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("/")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }


@router.get("/status")
async def get_status():
    """Get application status."""
    return {
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "components": {
            "ollama": settings.OLLAMA_BASE_URL,
            "database": "configured",
            "redis": settings.REDIS_URL,
            "mcp": "enabled" if settings.MCP_TOOLS_ENABLED else "disabled"
        }
    }
