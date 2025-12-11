from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_infer_emotion_invalid_payload():
    r = client.post("/v1/infer", json={"session_id": "s1", "context": {"x": "bad"}})
    assert r.status_code == 400
