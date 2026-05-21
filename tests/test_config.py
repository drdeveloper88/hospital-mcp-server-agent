"""
Unit tests for configuration.
"""
import pytest
from app.config import settings


def test_settings_loaded():
    """Test that settings are properly loaded."""
    assert settings.ENVIRONMENT in ["development", "production", "testing"]
    assert settings.OLLAMA_BASE_URL
    assert settings.DATABASE_URL
    assert settings.REDIS_URL


def test_model_settings():
    """Test LLM model settings."""
    assert settings.OLLAMA_MODEL
    assert settings.OLLAMA_EMBEDDING_MODEL


def test_agent_settings():
    """Test agent configuration."""
    assert settings.AGENT_TIMEOUT > 0
    assert settings.MAX_ITERATIONS > 0
    assert settings.SUPERVISOR_MODEL


def test_logging_settings():
    """Test logging configuration."""
    assert settings.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    assert settings.LOG_FORMAT in ["json", "text"]
    assert settings.LOG_OUTPUT in ["console", "file", "both"]
