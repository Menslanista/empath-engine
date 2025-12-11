package main

import (
    "testing"
    "google.golang.org/protobuf/encoding/protojson"
    pb "empathengine/llm-gateway/pkg/proto"
)

func TestProtoJSON(t *testing.T) {
    pred := &pb.EmotionPrediction{DominantEmotion: "engaged", Confidence: 0.85}
    b, err := protojson.Marshal(pred)
    if err != nil {
        t.Fatal(err)
    }
    var out pb.EmotionPrediction
    if err := protojson.Unmarshal(b, &out); err != nil {
        t.Fatal(err)
    }
    if out.GetDominantEmotion() != "engaged" {
        t.Fatal("unexpected")
    }
}

func TestParsePlayerBehaviorJSON_Invalid(t *testing.T) {
    _, err := converter.ParsePlayerBehaviorJSON([]byte("{"))
    if err == nil {
        t.Fatal("expected error")
    }
}
