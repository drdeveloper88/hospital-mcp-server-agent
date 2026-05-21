"""
Ollama LLM integration for hospital agent system.
"""
import logging
import httpx
from typing import AsyncGenerator, Dict, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama LLM."""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.embedding_model = settings.OLLAMA_EMBEDDING_MODEL
        self.timeout = httpx.Timeout(settings.MCP_TIMEOUT)
    
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        stream: bool = False
    ) -> AsyncGenerator[str, None] | str:
        """Generate response from Ollama."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "system": system or "",
                    "stream": stream
                }
                
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/generate",
                    json=payload
                ) as response:
                    if stream:
                        async for line in response.aiter_lines():
                            if line:
                                yield line
                    else:
                        data = await response.json()
                        return data.get("response", "")
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            raise
    
    async def embed(self, text: str) -> list:
        """Generate embeddings using Ollama."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/embeddings",
                    json={"model": self.embedding_model, "prompt": text}
                )
                data = response.json()
                return data.get("embedding", [])
        except Exception as e:
            logger.error(f"Ollama embedding error: {e}")
            raise

ollama_client = OllamaClient()
