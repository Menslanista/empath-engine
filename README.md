# Empath Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Microservices](https://img.shields.io/badge/Architecture-Microservices-green.svg)](https://microservices.io/)

**Empath Engine** is a sophisticated microservices-based platform for real-time emotion inference and adaptive narrative generation in interactive applications. Built with a polyglot architecture, it combines machine learning, behavioral analysis, and dynamic storytelling to create emotionally responsive experiences.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Services](#services)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Overview

Empath Engine analyzes player behavior in real-time to infer emotional states and dynamically adapt narrative content. The system processes behavioral data such as decision latency, action frequency, and contextual information to predict emotions with confidence scores, enabling applications to respond empathetically to user states.

### Key Capabilities

- **Real-time Emotion Inference**: Analyze player behavior patterns to predict emotional states
- **Adaptive Narrative Generation**: Dynamically adjust story content based on emotional context
- **Character Memory Management**: Maintain persistent character states and interaction history
- **Multi-LLM Gateway**: Unified interface for multiple language model providers
- **Scalable Microservices**: Independent services that can scale horizontally
- **Protocol Buffers**: Efficient inter-service communication with type-safe contracts

## Architecture

Empath Engine follows a microservices architecture with four core services communicating via REST APIs and Protocol Buffers:

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Application                       │
└────────────┬────────────────────────────────────────────────┘
             │
             ├──────────────┬──────────────┬──────────────┐
             │              │              │              │
             ▼              ▼              ▼              ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│    Emotion     │ │   Narrative    │ │  LLM Gateway   │ │   Character    │
│   Inference    │ │    Director    │ │                │ │     Memory     │
│   (Python)     │ │  (Node.js)     │ │      (Go)      │ │   (Python)     │
│   Port: 8000   │ │   Port: 3000   │ │   Port: 8080   │ │   Port: 8001   │
└────────┬───────┘ └────────┬───────┘ └────────┬───────┘ └────────┬───────┘
         │                  │                  │                  │
         └──────────────────┴──────────────────┴──────────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │     Redis     │
                            │  (Cache/Pub)  │
                            │  Port: 6379   │
                            └───────────────┘
```

### Service Responsibilities

| Service | Language | Port | Purpose |
|---------|----------|------|---------|
| **Emotion Inference** | Python (FastAPI) | 8000 | Analyzes behavioral data to predict emotional states |
| **Narrative Director** | Node.js (Express) | 3000 | Generates adaptive narrative content based on emotions |
| **LLM Gateway** | Go | 8080 | Unified interface for multiple LLM providers |
| **Character Memory** | Python (FastAPI) | 8001 | Manages persistent character states and memories |
| **Redis** | - | 6379 | Shared cache and pub/sub messaging |

## Features

### Emotion Inference Service
- Real-time behavioral pattern analysis
- Multi-dimensional emotion prediction
- Confidence scoring for predictions
- Support for contextual data enrichment
- Health and readiness endpoints

### Narrative Director Service
- Dynamic story adaptation
- Emotion-aware content generation
- Character interaction management
- Protocol Buffer integration

### LLM Gateway Service
- Multi-provider LLM support
- Request routing and load balancing
- Response caching
- Error handling and fallbacks

### Character Memory Service
- Persistent character state management
- Interaction history tracking
- Memory retrieval and querying
- RESTful API interface

## Technology Stack

### Languages & Frameworks
- **Python 3.11+**: FastAPI, Pydantic, Uvicorn
- **Node.js 18+**: Express.js, Jest
- **Go 1.20+**: Standard library, Protocol Buffers
- **Protocol Buffers 3**: Inter-service communication

### Infrastructure
- **Docker & Docker Compose**: Containerization and orchestration
- **Redis 7**: Caching and message broker
- **Make**: Build automation

### Development Tools
- **pytest**: Python testing
- **Jest**: JavaScript testing
- **Protocol Buffer Compiler**: Code generation

## Prerequisites

Ensure you have the following installed:

- **Docker** (v20.10+) and **Docker Compose** (v2.0+)
- **Python** (v3.11+)
- **Node.js** (v18+) and **npm** (v9+)
- **Go** (v1.20+)
- **Make** (for build automation)
- **Protocol Buffer Compiler** (`protoc`)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/empath-engine.git
cd empath-engine
```

### 2. Initialize the Project

```bash
make init
```

This command will:
- Install dependencies for all services
- Generate Protocol Buffer code
- Set up the development environment

### 3. Build Individual Services (Optional)

```bash
make build-emotion      # Build Emotion Inference service
make build-narrative    # Build Narrative Director service
make build-llm          # Build LLM Gateway service
make build-character    # Build Character Memory service
```

## Quick Start

### Using Docker Compose (Recommended)

```bash
make dev-up
```

This starts all services in detached mode. Services will be available at:
- Emotion Inference: http://localhost:8000
- Narrative Director: http://localhost:3000
- LLM Gateway: http://localhost:8080
- Character Memory: http://localhost:8001
- Redis: localhost:6379

### Verify Services

```bash
curl http://localhost:8000/health
curl http://localhost:3000/health
curl http://localhost:8080/health
curl http://localhost:8001/health
```

### Stop Services

```bash
make dev-down
```

## Services

### Emotion Inference Service

**Technology**: Python, FastAPI, Uvicorn

**Endpoints**:
- `GET /health` - Health check
- `GET /ready` - Readiness check
- `POST /infer` - Infer emotion from behavioral data

**Example Request**:
```bash
curl -X POST http://localhost:8000/infer \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user-123",
    "timestamp_ms": 1704067200000,
    "decision_latency_ms": 1250.5,
    "action_frequency": 15,
    "recent_choices": [1, 2, 1, 3, 2],
    "context_data": {
      "difficulty": 0.75,
      "progress": 0.45
    }
  }'
```

**Example Response**:
```json
{
  "dominant_emotion": "focused",
  "confidence": 0.87,
  "all_scores": {
    "focused": 0.87,
    "frustrated": 0.08,
    "excited": 0.05
  },
  "timestamp_ms": 1704067200000
}
```

### Narrative Director Service

**Technology**: Node.js, Express

**Endpoints**:
- `GET /health` - Health check
- `POST /generate` - Generate adaptive narrative content

**Features**:
- Emotion-aware story generation
- Character interaction management
- Protocol Buffer integration

### LLM Gateway Service

**Technology**: Go

**Endpoints**:
- `GET /health` - Health check
- `POST /complete` - LLM completion request

**Features**:
- Multi-provider support
- Request routing
- Response caching
- Error handling

### Character Memory Service

**Technology**: Python, FastAPI

**Endpoints**:
- `GET /health` - Health check
- `GET /memory` - Retrieve character memory

**Example Request**:
```bash
curl "http://localhost:8001/memory?character_id=npc-001&session_id=user-123"
```

**Example Response**:
```json
{
  "character_id": "npc-001",
  "session_id": "user-123",
  "interactions": 5,
  "last_emotion": "friendly",
  "memory_summary": "Player has been helpful and cooperative"
}
```

## API Documentation

### Protocol Buffer Definitions

The system uses Protocol Buffers for type-safe inter-service communication. The main message types are defined in `shared/proto/emotion.proto`:

```protobuf
message PlayerBehaviorData {
  string session_id = 1;
  int64 timestamp_ms = 2;
  float decision_latency_ms = 3;
  int32 action_frequency = 4;
  repeated int32 recent_choices = 5;
  map<string, float> context_data = 6;
}

message EmotionPrediction {
  string dominant_emotion = 1;
  float confidence = 2;
  map<string, float> all_scores = 3;
  int64 timestamp_ms = 4;
}
```

### Generating Protocol Buffer Code

```bash
make generate-proto
```

This generates language-specific code for:
- Python: `*_pb2.py` files
- Node.js: `*_pb.js` files
- Go: `*.pb.go` files

## Development

### Project Structure

```
empath-engine/
├── services/
│   ├── emotion-inference/      # Python FastAPI service
│   │   ├── src/
│   │   │   ├── main.py         # Service entry point
│   │   │   └── converters.py   # Proto converters
│   │   ├── tests/              # Unit tests
│   │   ├── requirements.txt    # Python dependencies
│   │   └── Dockerfile
│   ├── narrative-director/     # Node.js Express service
│   │   ├── src/
│   │   │   ├── index.js        # Service entry point
│   │   │   └── utils/
│   │   ├── tests/              # Unit tests
│   │   ├── package.json        # Node dependencies
│   │   └── Dockerfile
│   ├── llm-gateway/            # Go service
│   │   ├── cmd/
│   │   │   └── main.go         # Service entry point
│   │   ├── pkg/                # Go packages
│   │   ├── go.mod              # Go dependencies
│   │   └── Dockerfile
│   └── character-memory/       # Python FastAPI service
│       ├── src/
│       │   └── main.py         # Service entry point
│       ├── requirements.txt    # Python dependencies
│       └── Dockerfile
├── shared/
│   └── proto/
│       └── emotion.proto       # Protocol Buffer definitions
├── scripts/
│   ├── generate-proto.sh       # Proto generation (Unix)
│   └── generate-proto.bat      # Proto generation (Windows)
├── docker-compose.yml          # Service orchestration
├── Makefile                    # Build automation
└── README.md                   # This file
```

### Local Development

#### Emotion Inference Service

```bash
cd services/emotion-inference
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

#### Narrative Director Service

```bash
cd services/narrative-director
npm install
npm start
```

#### LLM Gateway Service

```bash
cd services/llm-gateway
go mod download
go run cmd/main.go
```

#### Character Memory Service

```bash
cd services/character-memory
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8001
```

## Testing

### Run All Tests

```bash
make test-emotion
```

### Service-Specific Tests

#### Emotion Inference

```bash
cd services/emotion-inference
pytest tests/ -v
```

#### Narrative Director

```bash
cd services/narrative-director
npm test
```

#### LLM Gateway

```bash
cd services/llm-gateway
go test ./...
```

## Deployment

### Docker Compose Production

```bash
docker-compose -f docker-compose.yml up -d
```

### Environment Variables

Create a `.env` file in the root directory:

```env
REDIS_HOST=redis
REDIS_PORT=6379
EMOTION_SERVICE_URL=http://emotion-inference:8000
NARRATIVE_SERVICE_URL=http://narrative-director:3000
LLM_SERVICE_URL=http://llm-gateway:8080
CHARACTER_SERVICE_URL=http://character-memory:8001
```

### Scaling Services

```bash
docker-compose up -d --scale emotion-inference=3
docker-compose up -d --scale narrative-director=2
```

## Configuration

### Service Ports

Default ports can be modified in `docker-compose.yml`:

```yaml
services:
  emotion-inference:
    ports:
      - "8000:8000"  # Change left side for host port
```

### Redis Configuration

Redis is configured with default settings. For production, consider:
- Enabling persistence
- Setting memory limits
- Configuring authentication

## Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Code Standards

- **Python**: Follow PEP 8, use type hints
- **JavaScript**: Follow ESLint configuration
- **Go**: Follow Go conventions, use `gofmt`
- **Commit Messages**: Use conventional commits format

### Testing Requirements

All PRs must include:
- Unit tests for new functionality
- Integration tests where applicable
- Documentation updates

## License

MIT License

Copyright (c) 2025 Synaptic Neuro-Gaming

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Support

For questions, issues, or feature requests:
- **Issues**: [GitHub Issues](https://github.com/yourusername/empath-engine/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/empath-engine/discussions)
- **Email**: support@synapticneurogaming.com

## Acknowledgments

Built with ❤️ by the Synaptic Wars team. https://synapticwars.com/

Special thanks to all contributors and the open-source community.
