from proto import emotion_pb2

def to_proto_player_behavior(data):
    ts = int((data.get("timestamp_ms") or 0))
    dl = float((data.get("decision_latency_ms") or 0.0))
    af = int((data.get("action_frequency") or 0))
    rc = [int(x) for x in (data.get("recent_choices") or [])]
    ctx = {str(k): float(v) for k, v in (data.get("context") or {}).items()}
    return emotion_pb2.PlayerBehaviorData(
        session_id=str(data.get("session_id")),
        timestamp_ms=ts,
        decision_latency_ms=dl,
        action_frequency=af,
        recent_choices=rc,
        context_data=ctx,
    )

def proto_to_response(pred: emotion_pb2.EmotionPrediction):
    return {
        "dominant_emotion": pred.dominant_emotion,
        "confidence": pred.confidence,
        "all_scores": dict(pred.all_scores),
        "timestamp_ms": pred.timestamp_ms,
    }
