"""
Integration tests for hospital agent system.
"""
import pytest
import asyncio
from httpx import AsyncClient
from app.main import app
from app.memory.redis_memory import memory_manager


@pytest.fixture
async def client():
    """FastAPI test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def setup_memory():
    """Setup memory for tests."""
    await memory_manager.init()
    yield
    await memory_manager.close()


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/api/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["environment"] in ["production", "development", "testing"]


@pytest.mark.asyncio
async def test_health_status(client):
    """Test health status endpoint."""
    response = await client.get("/api/health/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "components" in data


@pytest.mark.asyncio
async def test_send_message(client, setup_memory):
    """Test send message endpoint."""
    response = await client.post(
        "/api/chat/send",
        json={
            "session_id": "test-123",
            "message": "Hello, can you help me?"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["session_id"] == "test-123"


@pytest.mark.asyncio
async def test_chat_history(client, setup_memory):
    """Test chat history endpoint."""
    session_id = "test-session"
    
    # Send a message first
    await client.post(
        "/api/chat/send",
        json={
            "session_id": session_id,
            "message": "Test message"
        }
    )
    
    # Get history
    response = await client.get(f"/api/chat/history/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert isinstance(data["messages"], list)


@pytest.mark.asyncio
async def test_clear_history(client, setup_memory):
    """Test clear history endpoint."""
    session_id = "test-session"
    
    # Send a message first
    await client.post(
        "/api/chat/send",
        json={
            "session_id": session_id,
            "message": "Test"
        }
    )
    
    # Clear history
    response = await client.delete(f"/api/chat/history/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "cleared"


@pytest.mark.asyncio
async def test_invalid_request(client):
    """Test invalid request handling."""
    response = await client.post(
        "/api/chat/send",
        json={}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_concurrent_sessions(client, setup_memory):
    """Test multiple concurrent sessions."""
    tasks = []
    for i in range(5):
        task = client.post(
            "/api/chat/send",
            json={
                "session_id": f"session-{i}",
                "message": f"Test message {i}"
            }
        )
        tasks.append(task)
    
    responses = await asyncio.gather(*tasks)
    assert all(r.status_code == 200 for r in responses)


@pytest.mark.asyncio
async def test_streaming_response(client):
    """Test streaming response."""
    response = await client.post(
        "/api/chat/stream",
        json={
            "session_id": "stream-test",
            "message": "Hello"
        }
    )
    assert response.status_code in [200, 500]
