# Hospital MCP Agent System

Production-ready multi-agent hospital system with LangGraph, FastMCP, and Ollama.

## Features

- **LangGraph Multi-Agent Supervisor**: Coordinates multiple specialized agents
- **FastMCP Integration**: Tool access and management
- **Ollama LLM**: Local language model support
- **Redis Memory**: Distributed conversation memory
- **PostgreSQL**: Persistent data storage
- **Streaming Chat**: Real-time response streaming
- **Production-Ready**: Docker, logging, monitoring

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- 16GB+ RAM

### Setup

1. **Clone and setup**
```bash
git clone <repo>
cd hospital-mcp-server-agent
cp .env.example .env
```

2. **Start infrastructure**
```bash
docker-compose up -d
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Pull Ollama models**
```bash
ollama pull llama2:13b
ollama pull nomic-embed-text
```

5. **Run application**
```bash
python -m app.main
```

6. **Access services**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- PgAdmin: http://localhost:5050

## Architecture

### Project Structure

```
hospital-mcp-server-agent/
├── app/
│   ├── agents/          # Multi-agent system
│   │   └── supervisor.py    # LangGraph supervisor
│   ├── api/            # FastAPI routes
│   │   ├── chat_routes.py
│   │   └── health_routes.py
│   ├── llm/            # LLM integration
│   │   └── ollama_client.py
│   ├── memory/         # Memory management
│   │   ├── redis_memory.py
│   │   └── database_memory.py
│   ├── mcp/            # FastMCP server
│   │   └── server.py
│   ├── services/       # Business logic
│   │   └── chat_service.py
│   ├── config.py       # Configuration
│   ├── database.py     # Database setup
│   ├── logging_config.py
│   └── main.py         # FastAPI app
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

### Components

#### 1. **LangGraph Supervisor** (`agents/supervisor.py`)
- Routes tasks to specialized agents
- Patient Information Agent
- Appointment Scheduling Agent
- Prescription Management Agent
- General Information Agent

#### 2. **Memory System** (`memory/`)
- Redis-based session memory
- PostgreSQL persistent storage
- Configurable retention policies

#### 3. **Streaming Chat** (`services/chat_service.py`)
- Real-time response streaming
- Session-based conversations
- Context management

#### 4. **FastMCP Integration** (`mcp/server.py`)
- Patient information retrieval
- Appointment scheduling
- Medical records access
- Prescription creation

#### 5. **Ollama LLM** (`llm/ollama_client.py`)
- Local model support
- Streaming generation
- Embedding capabilities

## API Endpoints

### Chat
- `POST /api/chat/stream` - Stream chat response
- `POST /api/chat/send` - Send message
- `GET /api/chat/history/{session_id}` - Get conversation history
- `DELETE /api/chat/history/{session_id}` - Clear history

### Health
- `GET /api/health/` - Health check
- `GET /api/health/status` - Application status

## Configuration

Edit `.env` file to customize:

```env
# Ollama
OLLAMA_MODEL=llama2:13b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/hospital_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Agent
AGENT_TIMEOUT=60
MAX_ITERATIONS=10
```

## Deployment

### Docker

```bash
docker build -t hospital-agent .
docker run -p 8000:8000 hospital-agent
```

### Docker Compose

```bash
docker-compose up -d
```

## Development

### Add new agent
1. Create agent class in `agents/`
2. Add to supervisor graph in `agents/supervisor.py`
3. Register routes in `api/`

### Add new MCP tool
1. Register in `mcp/server.py`
2. Add handler function with `@server.call_tool()`

### Monitoring
- Check logs: `docker-compose logs -f app`
- Access PgAdmin: http://localhost:5050
- Health endpoint: http://localhost:8000/api/health/

## License

MIT
