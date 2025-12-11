@echo off
setlocal enabledelayedexpansion

set "PROTO_DIR=shared/proto"
set "OUT_DIR_PY=services\emotion-inference\src\proto"
set "OUT_DIR_GO=services\llm-gateway\pkg\proto"
set "OUT_DIR_JS=services\narrative-director\src\proto"

if not exist "!OUT_DIR_PY!" mkdir "!OUT_DIR_PY!" 2>nul
if not exist "!OUT_DIR_GO!" mkdir "!OUT_DIR_GO!" 2>nul
if not exist "!OUT_DIR_JS!" mkdir "!OUT_DIR_JS!" 2>nul

echo Generating Python protobuf files...
python -m grpc_tools.protoc -I"!PROTO_DIR!" --python_out="!OUT_DIR_PY!" --grpc_python_out="!OUT_DIR_PY!" "!PROTO_DIR!\*.proto"

if %ERRORLEVEL% NEQ 0 (
    echo Warning: Python protobuf generation failed
)

echo Generating Go protobuf files...
protoc -I"!PROTO_DIR!" --go_out="!OUT_DIR_GO!" --go-grpc_out="!OUT_DIR_GO!" "!PROTO_DIR!\*.proto"

if %ERRORLEVEL% NEQ 0 (
    echo Warning: Go protobuf generation failed
)

echo Generating JavaScript protobuf files...
protoc -I"!PROTO_DIR!" --js_out=import_style=commonjs:"!OUT_DIR_JS!" "!PROTO_DIR!\*.proto"

if %ERRORLEVEL% NEQ 0 (
    echo Warning: JavaScript protobuf generation failed
)

echo Protobuf generation completed.