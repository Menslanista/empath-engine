# Architecture Documentation

## System Overview

Empath Engine is a microservices-based platform designed for real-time emotion inference and adaptive narrative generation. The system processes player behavioral data to predict emotional states and dynamically adjusts narrative content to create emotionally responsive experiences.

## Design Principles

### 1. Microservices Architecture
- **Service Independence**: Each service can be developed, deployed, and scaled independently
- **Technology Diversity**: Services use the best technology for their specific purpose
- **Fault Isolation**: Failures in one service don't cascade to others
- **Scalability**: Individual services can scale based on demand

### 2. Event-Driven Communication
- **Asynchronous Processing**: Services communicate via events and messages
- **Loose Coupling**: Services don't need to know about each other's implementation
- **Resilience**: System continues operating even if some services are temporarily unavailable

### 3. Data Consistency
- **Eventually Consistent**: Services maintain their own data stores
- **Event Sourcing**: State changes are captured as events
- **CQRS Pattern**: Separation of read and write operations where appropriate

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Client Layer                                 │
│  (Game Engines, Web Apps, Mobile Apps)                              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTP/REST
                             │
┌────────────────────────────┴────────────────────────────────────────┐
│                      API Gateway (Future)                            │
│  - Authentication                                                    │
│  - Rate Limiting                                                     │
│  - Request Routing                                                   │
└────────────┬──────────────┬──────────────┬──────────────┬───────────┘
             │              │              │              │
             │              │              │              │
┌────────────▼──────┐ ┌────▼──────┐ ┌────▼──────┐ ┌────▼──────────┐
│  Emotion          │ │ Narrative │ │    LLM    │ │  Character    │
│  Inference        │ │ Director  │ │  Gateway  │ │   Memory      │
│                   │ │           │ │           │ │               │
│  - FastAPI        │ │ - Express │ │ - Go      │ │  - FastAPI    │
│  - Python 3.11    │ │ - Node.js │ │ - Go 1.20 │ │  - Python     │
│  - Port: 8000     │ │ - Port:   │ │ - Port:   │ │  - Port: 8001 │
│                   │ │   3000    │ │   8080    │ │               │
└────────────┬──────┘ └────┬──────┘ └────┬──────┘ └────┬──────────┘
             │              │              │              │
             └──────────────┴──────────────┴──────────────┘
                                    │
                                    │
                          ┌─────────▼─────────┐
                          │      Redis        │
                          │  - Cache          │
                          │  - Pub/Sub        │
                          │  - Session Store  │
                          └───────────────────┘
```

## Service Details

### 1. Emotion Inference Service

**Purpose**: Analyze player behavior patterns to predict emotional states

**Technology Stack**:
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Server**: Uvicorn (ASGI)
- **Dependencies**: Pydantic, Protocol Buffers

**Responsibilities**:
- Receive player behavioral data
- Process and normalize input data
- Apply emotion inference algorithms
- Return emotion predictions with confidence scores
- Cache recent predictions in Redis

**Data Flow**:
```
Client Request → FastAPI Endpoint → Data Validation (Pydantic)
    → Emotion Inference Logic → Redis Cache → Response
```

**Key Components**:
- `main.py`: Service entry point and API endpoints
- `converters.py`: Protocol Buffer conversion utilities
- `inference/`: Emotion inference algorithms
- `models/`: Data models and schemas

**Scaling Considerations**:
- Stateless design allows horizontal scaling
- CPU-intensive operations can be offloaded to workers
- Redis caching reduces redundant computations

---

### 2. Narrative Director Service

**Purpose**: Generate adaptive narrative content based on emotional context

**Technology Stack**:
- **Language**: JavaScript (Node.js 18+)
- **Framework**: Express.js
- **Dependencies**: google-protobuf

**Responsibilities**:
- Receive emotion data and narrative context
- Generate contextually appropriate narrative content
- Manage dialogue options and scene adjustments
- Coordinate with LLM Gateway for content generation
- Track narrative state in Redis

**Data Flow**:
```
Client Request → Express Middleware → Emotion Processing
    → LLM Gateway Request → Content Generation → Response
```

**Key Components**:
- `index.js`: Service entry point and routing
- `controllers/`: Request handlers
- `services/`: Business logic
- `utils/converters.js`: Data transformation utilities

**Scaling Considerations**:
- Asynchronous I/O for high concurrency
- Connection pooling for external services
- Caching of generated content

---

### 3. LLM Gateway Service

**Purpose**: Unified interface for multiple language model providers

**Technology Stack**:
- **Language**: Go 1.20+
- **Framework**: Standard library (net/http)
- **Dependencies**: google.golang.org/protobuf

**Responsibilities**:
- Route requests to appropriate LLM providers
- Handle authentication with LLM APIs
- Implement retry logic and fallbacks
- Cache responses to reduce API costs
- Monitor usage and rate limits

**Data Flow**:
```
Client Request → HTTP Handler → Provider Selection
    → LLM API Call → Response Caching → Response
```

**Key Components**:
- `cmd/main.go`: Service entry point
- `pkg/providers/`: LLM provider implementations
- `pkg/cache/`: Response caching logic
- `pkg/router/`: Request routing

**Scaling Considerations**:
- Goroutines for concurrent request handling
- Connection pooling for LLM APIs
- Distributed caching with Redis

---

### 4. Character Memory Service

**Purpose**: Manage persistent character states and interaction history

**Technology Stack**:
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Server**: Uvicorn (ASGI)

**Responsibilities**:
- Store character interaction history
- Track relationship levels and emotional states
- Provide memory retrieval APIs
- Maintain character consistency across sessions
- Persist data to Redis

**Data Flow**:
```
Client Request → FastAPI Endpoint → Redis Query
    → Data Aggregation → Response
```

**Key Components**:
- `main.py`: Service entry point and API endpoints
- `models/`: Character and memory data models
- `storage/`: Redis interaction layer

**Scaling Considerations**:
- Read-heavy workload optimized with caching
- Eventual consistency for memory updates
- Sharding by character_id for large datasets

---

### 5. Redis

**Purpose**: Shared cache, session store, and message broker

**Technology**: Redis 7 (Alpine)

**Use Cases**:
- **Caching**: Store frequently accessed data
- **Session Management**: Track user sessions
- **Pub/Sub**: Event broadcasting between services
- **Rate Limiting**: Track API usage

**Data Structures**:
- **Strings**: Simple key-value caching
- **Hashes**: Character memory storage
- **Sets**: Session tracking
- **Sorted Sets**: Rate limiting counters
- **Pub/Sub**: Event notifications

**Scaling Considerations**:
- Redis Cluster for horizontal scaling
- Redis Sentinel for high availability
- Persistence configuration for durability

## Communication Patterns

### 1. Synchronous Communication (REST)

Used for request-response interactions:
- Client → Services
- Service → Service (when immediate response needed)

**Advantages**:
- Simple to implement
- Easy to debug
- Immediate feedback

**Disadvantages**:
- Tight coupling
- Cascading failures
- Latency accumulation

### 2. Asynchronous Communication (Future)

Planned for event-driven interactions:
- Service → Redis Pub/Sub → Service
- Event sourcing for state changes

**Advantages**:
- Loose coupling
- Better fault tolerance
- Improved scalability

**Disadvantages**:
- Eventual consistency
- More complex debugging
- Message ordering challenges

## Data Models

### Protocol Buffer Definitions

```protobuf
// Player behavioral data
message PlayerBehaviorData {
  string session_id = 1;
  int64 timestamp_ms = 2;
  float decision_latency_ms = 3;
  int32 action_frequency = 4;
  repeated int32 recent_choices = 5;
  map<string, float> context_data = 6;
}

// Emotion prediction result
message EmotionPrediction {
  string dominant_emotion = 1;
  float confidence = 2;
  map<string, float> all_scores = 3;
  int64 timestamp_ms = 4;
}
```

### Data Flow

```
Player Action → Behavioral Data Collection → Emotion Inference
    → Emotion Prediction → Narrative Director → Adaptive Content
    → Character Memory Update → Client Response
```

## Security Architecture

### Current Implementation

- **Network Isolation**: Services communicate within Docker network
- **Input Validation**: Pydantic models validate all inputs
- **Error Handling**: Graceful error responses without sensitive data

### Future Enhancements

- **API Gateway**: Centralized authentication and authorization
- **JWT Tokens**: Stateless authentication
- **Rate Limiting**: Per-user and per-service limits
- **TLS/SSL**: Encrypted communication
- **Secret Management**: Vault integration for credentials

## Deployment Architecture

### Development Environment

```
Docker Compose
├── emotion-inference (container)
├── narrative-director (container)
├── llm-gateway (container)
├── character-memory (container)
└── redis (container)
```

### Production Environment (Future)

```
Kubernetes Cluster
├── Ingress Controller
├── API Gateway (Deployment)
├── Emotion Inference (Deployment, 3 replicas)
├── Narrative Director (Deployment, 2 replicas)
├── LLM Gateway (Deployment, 2 replicas)
├── Character Memory (Deployment, 2 replicas)
├── Redis (StatefulSet, 3 replicas)
└── Monitoring Stack (Prometheus, Grafana)
```

## Monitoring and Observability

### Metrics (Planned)

- **Service Metrics**: Request rate, latency, error rate
- **Business Metrics**: Emotion predictions, narrative generations
- **Infrastructure Metrics**: CPU, memory, network usage

### Logging

- **Structured Logging**: JSON format for all services
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Correlation IDs**: Track requests across services

### Tracing (Planned)

- **Distributed Tracing**: OpenTelemetry integration
- **Span Tracking**: Monitor request flow through services
- **Performance Analysis**: Identify bottlenecks

## Disaster Recovery

### Backup Strategy

- **Redis Snapshots**: Periodic RDB snapshots
- **Configuration Backups**: Version-controlled configs
- **Database Backups**: Regular backups of persistent data

### Recovery Procedures

1. **Service Failure**: Automatic restart via Docker/Kubernetes
2. **Data Loss**: Restore from latest Redis snapshot
3. **Complete Outage**: Rebuild from infrastructure as code

## Performance Optimization

### Caching Strategy

- **L1 Cache**: In-memory caching within services
- **L2 Cache**: Redis for shared caching
- **Cache Invalidation**: TTL-based and event-driven

### Database Optimization

- **Connection Pooling**: Reuse database connections
- **Query Optimization**: Indexed queries for fast retrieval
- **Data Partitioning**: Shard by session_id or character_id

### Network Optimization

- **HTTP/2**: Multiplexed connections
- **Compression**: Gzip for large responses
- **CDN**: Static content delivery (future)

## Future Enhancements

### Short-term (3-6 months)

- API Gateway implementation
- Authentication and authorization
- Comprehensive monitoring stack
- Integration tests suite

### Medium-term (6-12 months)

- Kubernetes deployment
- Event-driven architecture
- Machine learning model improvements
- SDK development (Python, JavaScript, Unity, Unreal)

### Long-term (12+ months)

- Multi-region deployment
- Real-time analytics dashboard
- Advanced emotion models
- Voice and facial expression analysis

## References

- [Microservices Patterns](https://microservices.io/patterns/index.html)
- [Protocol Buffers Documentation](https://protobuf.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Express.js Documentation](https://expressjs.com/)
- [Go Documentation](https://go.dev/doc/)
- [Redis Documentation](https://redis.io/documentation)

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Maintainer**: Synaptic Neuro-Gaming Team
