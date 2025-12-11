from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import time
from proto import emotion_pb2
from .converters import to_proto_player_behavior, proto_to_response

class PlayerBehaviorData(BaseModel):
    session_id: str
    timestamp_ms: int | None = None
    decision_latency_ms: float | None = None
    action_frequency: int | None = None
    recent_choices: list[int] | None = None
    context: dict | None = None

class EmotionPrediction(BaseModel):
    dominant_emotion: str
    confidence: float
    all_scores: dict
    timestamp_ms: int

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/ready")
async def ready():
    return {"status": "ready"}

@app.post("/v1/infer")
async def infer_emotion(data: PlayerBehaviorData, request: Request):
    try:
        ts = data.timestamp_ms or int(time.time() * 1000)
        pb = to_proto_player_behavior({
            "session_id": data.session_id,
            "timestamp_ms": ts,
            "decision_latency_ms": data.decision_latency_ms,
            "action_frequency": data.action_frequency,
            "recent_choices": data.recent_choices,
            "context": data.context,
        })
    except Exception:
        raise HTTPException(status_code=400, detail="invalid payload")
    pred = emotion_pb2.EmotionPrediction(
        dominant_emotion="engaged",
        confidence=0.85,
        all_scores={"engaged": 0.7, "frustrated": 0.2, "curious": 0.1},
        timestamp_ms=pb.timestamp_ms or ts
    )
    return proto_to_response(pred)
