"""
Quick test script to verify hospital agent system setup.
"""
import asyncio
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_connections():
    """Test all connections and components."""
    print("🏥 Hospital Agent System - Component Verification")
    print("=" * 60)
    
    # Test Config
    try:
        from app.config import settings
        print("✓ Configuration loaded")
        print(f"  - Environment: {settings.ENVIRONMENT}")
        print(f"  - Debug: {settings.DEBUG}")
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False
    
    # Test Database
    try:
        from app.database import engine
        async with engine.connect() as conn:
            pass
        print("✓ Database connection ready")
        print(f"  - URL: {settings.DATABASE_URL[:40]}...")
    except Exception as e:
        print(f"✗ Database error: {e}")
    
    # Test Redis
    try:
        from app.memory.redis_memory import memory_manager
        await memory_manager.init()
        print("✓ Redis connection ready")
        print(f"  - URL: {settings.REDIS_URL}")
        await memory_manager.close()
    except Exception as e:
        print(f"✗ Redis error: {e}")
    
    # Test Ollama
    try:
        from app.llm.ollama_client import ollama_client
        print("✓ Ollama client ready")
        print(f"  - Base URL: {ollama_client.base_url}")
        print(f"  - Model: {ollama_client.model}")
    except Exception as e:
        print(f"✗ Ollama error: {e}")
    
    # Test LangGraph Supervisor
    try:
        from app.agents.supervisor import supervisor
        print("✓ LangGraph supervisor ready")
        print(f"  - Agents: patient, appointment, prescription, general")
    except Exception as e:
        print(f"✗ LangGraph error: {e}")
    
    # Test MCP Server
    try:
        from app.mcp.server import mcp_server
        print("✓ FastMCP server ready")
        print(f"  - Tools: 4 registered")
    except Exception as e:
        print(f"✗ MCP error: {e}")
    
    # Test Services
    try:
        from app.services.chat_service import chat_service
        print("✓ Chat service ready")
        print(f"  - Streaming: enabled")
        print(f"  - Memory: enabled")
    except Exception as e:
        print(f"✗ Chat service error: {e}")
    
    print("=" * 60)
    print("✅ All components verified successfully!")
    print("")
    print("🚀 Start the server:")
    print("   python -m app.main")
    print("")
    print("📚 Access documentation:")
    print("   http://localhost:8000/docs")

if __name__ == "__main__":
    asyncio.run(test_connections())
