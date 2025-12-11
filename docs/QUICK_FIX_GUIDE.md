# 🚀 Quick Fix Guide - Get Empath Engine Running

**Time Required**: 30-60 minutes  
**Difficulty**: Intermediate

---

## ⚠️ Current Status

**Build Status**: ❌ BROKEN  
**Reason**: Missing Protocol Buffer tools

---

## 🎯 Goal

Get the project building and all services running locally.

---

## 📋 Prerequisites

Before starting, ensure you have:
- [ ] Windows 10/11, Linux, or macOS
- [ ] Administrator/sudo access
- [ ] Internet connection
- [ ] 2GB free disk space

---

## 🔧 Step 1: Install Protocol Buffer Compiler (5 min)

### Windows
```powershell
# Download protoc
# Go to: https://github.com/protocolbuffers/protobuf/releases
# Download: protoc-25.1-win64.zip (or latest)

# Extract to C:\protoc
# Add to PATH:
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\protoc\bin", "User")

# Restart terminal and verify:
protoc --version
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y protobuf-compiler
protoc --version
```

### macOS
```bash
brew install protobuf
protoc --version
```

**Expected Output**: `libprotoc 3.x.x` or `libprotoc 4.x.x`

---

## 🐍 Step 2: Fix Python Setup (10 min)

### Install Python 3.11+ (if needed)
```bash
# Check current version
python --version

# If < 3.11, download from python.org
# Or use pyenv:
pyenv install 3.11
pyenv local 3.11
```

### Install Missing Python Package
```bash
cd empath-engine

# Install grpcio-tools (CRITICAL - missing from requirements.txt)
pip install grpcio-tools

# Verify
python -m grpc_tools.protoc --version
```

### Update requirements.txt
Add this line to both:
- `services/emotion-inference/requirements.txt`
- `services/character-memory/requirements.txt`

```txt
grpcio-tools==1.60.0
```

---

## 🟢 Step 3: Fix Go Setup (10 min)

### Install Go Protobuf Plugins
```bash
# Install plugins
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Add to PATH (if not already)
# Windows:
set PATH=%PATH%;%USERPROFILE%\go\bin

# Linux/Mac:
export PATH=$PATH:$(go env GOPATH)/bin
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc

# Verify
protoc-gen-go --version
```

---

## 📦 Step 4: Fix Node.js Setup (5 min)

### Install JavaScript Protobuf Plugin
```bash
# Option 1: Global install (recommended)
npm install -g protoc-gen-js

# Option 2: Local install
cd services/narrative-director
npm install --save-dev protoc-gen-js

# Verify
protoc-gen-js --version
```

---

## 🔄 Step 5: Generate Protocol Buffer Code (2 min)

```bash
cd empath-engine

# Create proto output directories
mkdir -p services/emotion-inference/proto
mkdir -p services/llm-gateway/pkg/proto
mkdir -p services/narrative-director/src/proto

# Generate code
cd shared/proto

# Python
protoc --python_out=../../services/emotion-inference/proto emotion.proto

# Go
protoc --go_out=../../services/llm-gateway/pkg/proto --go_opt=paths=source_relative emotion.proto

# JavaScript
protoc --js_out=import_style=commonjs:../../services/narrative-director/src/proto emotion.proto

# Verify files were created
ls ../../services/emotion-inference/proto/emotion_pb2.py
ls ../../services/llm-gateway/pkg/proto/emotion.pb.go
ls ../../services/narrative-director/src/proto/emotion_pb.js
```

**Expected**: All three files should exist

---

## 🏃 Step 6: Start Services (5 min)

### Terminal 1: Redis
```bash
docker run -d -p 6379:6379 redis:7-alpine
# Or if you have Redis installed:
redis-server
```

### Terminal 2: Emotion Inference (Python)
```bash
cd empath-engine/services/emotion-inference
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

### Terminal 3: Narrative Director (Node.js)
```bash
cd empath-engine/services/narrative-director
npm install
npm start
```

### Terminal 4: LLM Gateway (Go)
```bash
cd empath-engine/services/llm-gateway
go mod download
go run cmd/main.go
```

### Terminal 5: Character Memory (Python)
```bash
cd empath-engine/services/character-memory
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8001
```

---

## ✅ Step 7: Verify Everything Works (2 min)

### Test Health Endpoints
```bash
# Emotion Inference
curl http://localhost:8000/health
# Expected: {"status":"ok"}

# Narrative Director
curl http://localhost:3000/health
# Expected: {"status":"ok"}

# LLM Gateway
curl http://localhost:8080/health
# Expected: {"status":"ok"}

# Character Memory
curl http://localhost:8001/health
# Expected: {"status":"ok"}
```

### Test API Endpoint
```bash
curl -X POST http://localhost:8000/v1/infer \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-123",
    "decision_latency_ms": 150.5,
    "action_frequency": 10,
    "recent_choices": [1, 2, 3],
    "context": {"level": 1}
  }'

# Expected: JSON response with emotion prediction
```

---

## 🎉 Success!

If all health checks return `{"status":"ok"}`, you're done!

---

## 🐛 Troubleshooting

### Issue: "protoc: command not found"
**Fix**: Restart terminal after installing protoc, or manually add to PATH

### Issue: "ModuleNotFoundError: No module named 'grpc_tools'"
**Fix**: Run `pip install grpcio-tools`

### Issue: "protoc-gen-go: program not found"
**Fix**: 
```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
export PATH=$PATH:$(go env GOPATH)/bin
```

### Issue: "Cannot find module './proto/emotion_pb.js'"
**Fix**: Regenerate JavaScript proto files:
```bash
cd shared/proto
protoc --js_out=import_style=commonjs:../../services/narrative-director/src/proto emotion.proto
```

### Issue: Python version error
**Fix**: Either upgrade to Python 3.11+ or change code syntax:
```python
# Change from:
timestamp_ms: int | None = None

# To:
from typing import Optional
timestamp_ms: Optional[int] = None
```

### Issue: Port already in use
**Fix**: 
```bash
# Find process using port (example: 8000)
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :8000
kill -9 <PID>
```

---

## 📚 Next Steps

Once everything is running:

1. **Read the Analysis**
   - See `ANALYSIS_SUMMARY.md` for overview
   - See `PROJECT_ANALYSIS.md` for detailed findings

2. **Fix Critical Issues**
   - Add authentication
   - Replace mock responses
   - Add error handling
   - Increase test coverage

3. **Improve Security**
   - Enable HTTPS
   - Add rate limiting
   - Add input validation

4. **Set Up Development Environment**
   - Configure IDE
   - Set up debugging
   - Install recommended extensions

---

## 🆘 Still Having Issues?

1. Check `SETUP_TROUBLESHOOTING.md` for detailed solutions
2. Review `Protobuf.txt` for your specific error
3. Verify all prerequisites are installed
4. Try the Docker approach instead:
   ```bash
   docker-compose up -d
   ```

---

## 📊 What You've Accomplished

- ✅ Installed Protocol Buffer compiler
- ✅ Installed all language-specific protobuf plugins
- ✅ Generated Protocol Buffer code for all services
- ✅ Started all 4 microservices
- ✅ Verified services are healthy

**Time Spent**: ~30-60 minutes  
**Status**: 🟢 Development environment ready!

---

## 🎯 Your Next Mission

Now that the project builds, focus on:

1. **Security** (Week 1-2)
   - Add JWT authentication
   - Add rate limiting

2. **Real Logic** (Week 3-6)
   - Replace mock emotion inference
   - Build narrative system

3. **Testing** (Week 7-9)
   - Write unit tests
   - Add integration tests

4. **Production** (Week 10-16)
   - Set up monitoring
   - Deploy to cloud

See `ANALYSIS_SUMMARY.md` for the complete roadmap.

---

**Good luck! 🚀**
