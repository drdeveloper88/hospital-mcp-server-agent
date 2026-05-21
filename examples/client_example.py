"""
Example client for interacting with hospital agent system.
"""
import httpx
import asyncio
import json
from typing import AsyncGenerator


class HospitalAgentClient:
    """Client for hospital agent API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = "example-session"
    
    async def stream_response(
        self,
        message: str,
        system_prompt: str = "You are a helpful hospital assistant"
    ) -> AsyncGenerator[str, None]:
        """Stream response from agent."""
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat/stream",
                json={
                    "session_id": self.session_id,
                    "message": message,
                    "system_prompt": system_prompt
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        yield line
    
    async def send_message(self, message: str) -> dict:
        """Send message and get response."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/chat/send",
                json={
                    "session_id": self.session_id,
                    "message": message
                }
            )
            return response.json()
    
    async def get_history(self) -> list:
        """Get conversation history."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/chat/history/{self.session_id}"
            )
            return response.json()
    
    async def clear_history(self) -> dict:
        """Clear conversation history."""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/api/chat/history/{self.session_id}"
            )
            return response.json()
    
    async def health_check(self) -> dict:
        """Check application health."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/health/"
            )
            return response.json()


async def main():
    """Example usage."""
    client = HospitalAgentClient()
    
    print("🏥 Hospital Agent System - Example Client")
    print("=" * 60)
    
    # Health check
    print("\n1️⃣  Health Check")
    health = await client.health_check()
    print(f"Status: {health.get('status')}")
    
    # Stream chat
    print("\n2️⃣  Streaming Chat Example")
    print("Message: 'Schedule an appointment with cardiology'")
    print("Response: ", end="", flush=True)
    
    async for chunk in client.stream_response(
        "Schedule an appointment with cardiology"
    ):
        print(chunk, end="", flush=True)
    print("\n")
    
    # Send message
    print("\n3️⃣  Non-Streaming Chat Example")
    print("Message: 'What are my medical records?'")
    response = await client.send_message("What are my medical records?")
    print(f"Response: {response['response'][:100]}...")
    print(f"Messages in session: {response['messages_count']}")
    
    # Get history
    print("\n4️⃣  Conversation History")
    history = await client.get_history()
    print(f"Total messages: {history['count']}")
    for i, msg in enumerate(history['messages'][-2:]):
        role = msg['role'].upper()
        content = msg['content']
        print(f"  {i+1}. [{role}] {content[:50]}...")
    
    print("\n" + "=" * 60)
    print("✅ Example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
