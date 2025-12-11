# API Reference

## Overview

Empath Engine provides RESTful APIs for all microservices. This document details the endpoints, request/response formats, and usage examples.

## Base URLs

| Service | Base URL | Port |
|---------|----------|------|
| Emotion Inference | `http://localhost:8000` | 8000 |
| Narrative Director | `http://localhost:3000` | 3000 |
| LLM Gateway | `http://localhost:8080` | 8080 |
| Character Memory | `http://localhost:8001` | 8001 |

## Authentication

Currently, the services do not require authentication for local development. For production deployments, implement API key authentication or OAuth 2.0.

---

## Emotion Inference Service

### Health Check

**Endpoint**: `GET /health`

**Description**: Check if the service is running

**Response**:
```json
{
  "status": "healthy"
}
```

**Status Codes**:
- `200 OK` - Service is healthy

**Example**:
```bash
curl http://localhost:8000/health
```

---

### Readiness Check

**Endpoint**: `GET /ready`

**Description**: Check if the service is ready to accept requests

**Response**:
```json
{
  "status": "ready"
}
```

**Status Codes**:
- `200 OK` - Service is ready

**Example**:
```bash
curl http://localhost:8000/ready
```

---

### Infer Emotion

**Endpoint**: `POST /infer`

**Description**: Analyze player behavior data and predict emotional state

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "session_id": "string",
  "timestamp_ms": 0,
  "decision_latency_ms": 0.0,
  "action_frequency": 0,
  "recent_choices": [0, 0, 0],
  "context_data": {
    "key": 0.0
  }
}
```

**Request Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | Yes | Unique identifier for the player session |
| `timestamp_ms` | integer | Yes | Unix timestamp in milliseconds |
| `decision_latency_ms` | float | Yes | Average time taken for decisions (ms) |
| `action_frequency` | integer | Yes | Number of actions in time window |
| `recent_choices` | array[integer] | Yes | Recent player choices/actions |
| `context_data` | object | No | Additional contextual information |

**Response**:
```json
{
  "dominant_emotion": "string",
  "confidence": 0.0,
  "all_scores": {
    "emotion_name": 0.0
  },
  "timestamp_ms": 0
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `dominant_emotion` | string | Primary detected emotion |
| `confidence` | float | Confidence score (0.0-1.0) |
| `all_scores` | object | Scores for all detected emotions |
| `timestamp_ms` | integer | Prediction timestamp |

**Status Codes**:
- `200 OK` - Successful prediction
- `400 Bad Request` - Invalid input data
- `500 Internal Server Error` - Processing error

**Example**:
```bash
curl -X POST http://localhost:8000/infer \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "player-abc-123",
    "timestamp_ms": 1704067200000,
    "decision_latency_ms": 1250.5,
    "action_frequency": 15,
    "recent_choices": [1, 2, 1, 3, 2],
    "context_data": {
      "difficulty": 0.75,
      "progress": 0.45,
      "health": 0.80
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

**Emotion Types**:
- `focused` - High concentration, steady actions
- `frustrated` - Erratic behavior, high latency
- `excited` - High action frequency, low latency
- `calm` - Steady, measured actions
- `anxious` - Variable latency, inconsistent choices
- `bored` - Low action frequency, high latency

---

## Narrative Director Service

### Health Check

**Endpoint**: `GET /health`

**Description**: Check if the service is running

**Response**:
```json
{
  "status": "healthy"
}
```

**Status Codes**:
- `200 OK` - Service is healthy

**Example**:
```bash
curl http://localhost:3000/health
```

---

### Generate Narrative

**Endpoint**: `POST /generate`

**Description**: Generate adaptive narrative content based on emotional state

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "emotion_data": {
    "dominant_emotion": "string",
    "confidence": 0.0
  },
  "context": {
    "scene_id": "string",
    "character_id": "string",
    "previous_choices": []
  }
}
```

**Request Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `emotion_data` | object | Yes | Emotion prediction from inference service |
| `emotion_data.dominant_emotion` | string | Yes | Primary detected emotion |
| `emotion_data.confidence` | float | Yes | Confidence score |
| `context` | object | Yes | Narrative context information |
| `context.scene_id` | string | Yes | Current scene identifier |
| `context.character_id` | string | No | Active character identifier |
| `context.previous_choices` | array | No | Previous player choices |

**Response**:
```json
{
  "narrative_content": "string",
  "dialogue_options": ["string"],
  "scene_adjustments": {
    "tone": "string",
    "pacing": "string"
  },
  "timestamp_ms": 0
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `narrative_content` | string | Generated narrative text |
| `dialogue_options` | array[string] | Available dialogue choices |
| `scene_adjustments` | object | Recommended scene modifications |
| `timestamp_ms` | integer | Generation timestamp |

**Status Codes**:
- `200 OK` - Successful generation
- `400 Bad Request` - Invalid input
- `500 Internal Server Error` - Generation error

**Example**:
```bash
curl -X POST http://localhost:3000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "emotion_data": {
      "dominant_emotion": "focused",
      "confidence": 0.87
    },
    "context": {
      "scene_id": "chapter1-scene3",
      "character_id": "npc-mentor",
      "previous_choices": ["help", "investigate"]
    }
  }'
```

**Example Response**:
```json
{
  "narrative_content": "The mentor notices your intense concentration and adjusts their teaching pace accordingly.",
  "dialogue_options": [
    "I'm ready for the next challenge",
    "Let me practice this technique more",
    "Can you explain that again?"
  ],
  "scene_adjustments": {
    "tone": "supportive",
    "pacing": "measured"
  },
  "timestamp_ms": 1704067200000
}
```

---

## LLM Gateway Service

### Health Check

**Endpoint**: `GET /health`

**Description**: Check if the service is running

**Response**:
```json
{
  "status": "healthy"
}
```

**Status Codes**:
- `200 OK` - Service is healthy

**Example**:
```bash
curl http://localhost:8080/health
```

---

### Complete Request

**Endpoint**: `POST /complete`

**Description**: Send completion request to configured LLM provider

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "prompt": "string",
  "max_tokens": 0,
  "temperature": 0.0,
  "provider": "string"
}
```

**Request Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | Yes | Input prompt for the LLM |
| `max_tokens` | integer | No | Maximum tokens to generate (default: 100) |
| `temperature` | float | No | Sampling temperature 0.0-1.0 (default: 0.7) |
| `provider` | string | No | Specific LLM provider to use |

**Response**:
```json
{
  "completion": "string",
  "provider": "string",
  "tokens_used": 0,
  "timestamp_ms": 0
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `completion` | string | Generated completion text |
| `provider` | string | LLM provider used |
| `tokens_used` | integer | Number of tokens consumed |
| `timestamp_ms` | integer | Completion timestamp |

**Status Codes**:
- `200 OK` - Successful completion
- `400 Bad Request` - Invalid request
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Provider error

**Example**:
```bash
curl -X POST http://localhost:8080/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Generate a supportive message for a focused player",
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

**Example Response**:
```json
{
  "completion": "You're doing great! Your concentration is impressive. Keep up the excellent work.",
  "provider": "openai",
  "tokens_used": 18,
  "timestamp_ms": 1704067200000
}
```

---

## Character Memory Service

### Health Check

**Endpoint**: `GET /health`

**Description**: Check if the service is running

**Response**:
```json
{
  "status": "healthy"
}
```

**Status Codes**:
- `200 OK` - Service is healthy

**Example**:
```bash
curl http://localhost:8001/health
```

---

### Get Character Memory

**Endpoint**: `GET /memory`

**Description**: Retrieve character memory and interaction history

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `character_id` | string | Yes | Character identifier |
| `session_id` | string | Yes | Player session identifier |

**Response**:
```json
{
  "character_id": "string",
  "session_id": "string",
  "interactions": 0,
  "last_emotion": "string",
  "memory_summary": "string",
  "relationship_level": 0.0,
  "key_events": ["string"]
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `character_id` | string | Character identifier |
| `session_id` | string | Session identifier |
| `interactions` | integer | Number of interactions |
| `last_emotion` | string | Last detected player emotion |
| `memory_summary` | string | Summary of interactions |
| `relationship_level` | float | Relationship score (0.0-1.0) |
| `key_events` | array[string] | Important interaction events |

**Status Codes**:
- `200 OK` - Memory retrieved successfully
- `404 Not Found` - Character or session not found
- `500 Internal Server Error` - Retrieval error

**Example**:
```bash
curl "http://localhost:8001/memory?character_id=npc-mentor&session_id=player-abc-123"
```

**Example Response**:
```json
{
  "character_id": "npc-mentor",
  "session_id": "player-abc-123",
  "interactions": 12,
  "last_emotion": "focused",
  "memory_summary": "Player has been diligent and attentive during training sessions. Shows strong commitment to learning.",
  "relationship_level": 0.75,
  "key_events": [
    "Completed first training challenge",
    "Asked insightful questions",
    "Helped another student"
  ]
}
```

---

## Error Responses

All services follow a consistent error response format:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

**Common Error Codes**:

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Request validation failed |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

**Example Error Response**:
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Missing required field: session_id",
    "details": {
      "field": "session_id",
      "expected": "string"
    }
  }
}
```

---

## Rate Limiting

Services implement rate limiting to ensure fair usage:

| Service | Rate Limit | Window |
|---------|------------|--------|
| Emotion Inference | 100 requests | 1 minute |
| Narrative Director | 50 requests | 1 minute |
| LLM Gateway | 20 requests | 1 minute |
| Character Memory | 100 requests | 1 minute |

**Rate Limit Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704067260
```

---

## Webhooks

Future versions will support webhooks for real-time event notifications.

---

## SDK Support

Official SDKs are planned for:
- Python
- JavaScript/TypeScript
- Unity (C#)
- Unreal Engine (C++)

---

## Versioning

The API follows semantic versioning. Current version: **v1**

Breaking changes will be introduced in new major versions with deprecation notices.

---

## Support

For API questions or issues:
- GitHub Issues: [Report a bug](https://github.com/yourusername/empath-engine/issues)
- Documentation: [Full docs](https://docs.empathengine.io)
- Email: api-support@synapticneurogaming.com
