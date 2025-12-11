#!/bin/bash
set -e
PROTO_DIR="shared/proto"
OUT_DIR_PY="services/emotion-inference/src/proto"
OUT_DIR_GO="services/llm-gateway/pkg/proto"
OUT_DIR_JS="services/narrative-director/src/proto"

mkdir -p "$OUT_DIR_PY" "$OUT_DIR_GO" "$OUT_DIR_JS"

python -m grpc_tools.protoc -I"$PROTO_DIR" --python_out="$OUT_DIR_PY" --grpc_python_out="$OUT_DIR_PY" "$PROTO_DIR"/*.proto || true

protoc -I"$PROTO_DIR" --go_out="$OUT_DIR_GO" --go-grpc_out="$OUT_DIR_GO" "$PROTO_DIR"/*.proto || true

protoc -I"$PROTO_DIR" --js_out=import_style=commonjs:"$OUT_DIR_JS" "$PROTO_DIR"/*.proto || true
