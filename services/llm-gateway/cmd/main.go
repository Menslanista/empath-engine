package main

import (
    "io"
    "net/http"
    pb "empathengine/llm-gateway/pkg/proto"
    "empathengine/llm-gateway/pkg/converter"
)

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        w.Write([]byte(`{"status":"ok"}`))
    })
    mux.HandleFunc("/v1/proxy", func(w http.ResponseWriter, r *http.Request) {
        defer r.Body.Close()
        body, _ := io.ReadAll(r.Body)
        data, err := converter.ParsePlayerBehaviorJSON(body)
        if err != nil {
            w.WriteHeader(http.StatusBadRequest)
            w.Write([]byte(`{"error":"invalid payload"}`))
            return
        }
        pred := &pb.EmotionPrediction{DominantEmotion: "engaged", Confidence: 0.85, TimestampMs: data.TimestampMs}
        b, _ := converter.ToEmotionPredictionJSON(pred)
        w.Header().Set("Content-Type", "application/json")
        w.Write(b)
    })
    http.ListenAndServe(":8080", mux)
}
