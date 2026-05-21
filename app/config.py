"""
Application core configuration and settings.
"""
from pydantic_settings import BaseSettings
from typing import Literal
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # API
    ENVIRONMENT: Literal["development", "production", "testing"] = "production"
    DEBUG: bool = False
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    WORKERS: int = 4
    
    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama2:13b"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"
    
    # Database
    DATABASE_URL: str = "postgresql://hospital_user:hospital_pass_123@localhost:5432/hospital_db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_DB: int = 0
    CACHE_TTL: int = 3600
    
    # Memory
    MEMORY_TYPE: Literal["redis", "database", "memory"] = "redis"
    MAX_MEMORY_SIZE: int = 1000
    MEMORY_RETENTION_DAYS: int = 30
    
    # MCP
    MCP_TOOLS_ENABLED: bool = True
    MCP_TIMEOUT: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: Literal["json", "text"] = "json"
    LOG_OUTPUT: Literal["console", "file", "both"] = "both"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Agent
    SUPERVISOR_MODEL: str = "ollama"
    AGENT_TIMEOUT: int = 60
    MAX_ITERATIONS: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
