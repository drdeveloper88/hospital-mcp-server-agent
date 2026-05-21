#!/bin/bash

# Hospital MCP Agent System Setup Script

set -e

echo "🏥 Hospital MCP Agent System Setup"
echo "===================================="

# Check dependencies
echo "✓ Checking dependencies..."
command -v docker >/dev/null 2>&1 || { echo "Docker required"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose required"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3.11+ required"; exit 1; }

# Create .env if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data

# Start infrastructure
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to be ready..."
sleep 10

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Pull Ollama models
echo "🤖 Pulling Ollama models..."
ollama pull llama2:13b
ollama pull nomic-embed-text

# Initialize database
echo "🗄️  Initializing database..."
python -c "
import asyncio
from app.database import init_db
asyncio.run(init_db())
"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Start the application:"
echo "   python -m app.main"
echo ""
echo "📚 API Documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "🏥 Health Check:"
echo "   http://localhost:8000/api/health/"
