package converter

import (
    "google.golang.org/protobuf/encoding/protojson"
    pb "empathengine/llm-gateway/pkg/proto"
)

var um = protojson.UnmarshalOptions{DiscardUnknown: true}
var mo = protojson.MarshalOptions{EmitUnpopulated: true}

func ParsePlayerBehaviorJSON(b []byte) (*pb.PlayerBehaviorData, error) {
    var d pb.PlayerBehaviorData
    if err := um.Unmarshal(b, &d); err != nil {
        return nil, err
    }
    return &d, nil
}

func ToEmotionPredictionJSON(pred *pb.EmotionPrediction) ([]byte, error) {
    return mo.Marshal(pred)
}
