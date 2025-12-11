from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_infer_emotion_serialization():
    data = {"session_id": "s1", "decision_latency_ms": 100.0, "action_frequency": 2, "recent_choices": [1,2], "context": {"x": 1.0}}
    r = client.post("/v1/infer", json=data)
    assert r.status_code == 200
    j = r.json()
    assert "dominant_emotion" in j
    assert "confidence" in j
