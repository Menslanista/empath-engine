# Empath Engine - Setup & Troubleshooting Guide

**Last Updated**: January 2025  
**Status**: 🔴 Critical Setup Issues Identified

---

## 🚨 Critical Issues Found

Based on analysis of the build logs (`Protobuf.txt`), the project currently **cannot build** due to missing Protocol Buffer tooling.

---

## 1. Protocol Buffer Setup Issues

### Issue 1: Python gRPC Tools Missing

**Error**:
```
ModuleNotFoundError: No module named 'grpc_tools'
```

**Cause**: The `grpcio-tools` package is not installed, which is required to generate Python Protocol Buffer code.

**Solution**:
```bash
# Install gRPC tools for Python
pip install grpcio-tools

# Verify installation
python -m grpc_tools.protoc --version
```

**Add to requirements.txt**:
```txt
grpcio-tools==1.60.0
```

---

### Issue 2: Go Protobuf Plugin Missing

**Error**:
```
'protoc-gen-go' is not recognized as an internal or external command
--go_out: protoc-gen-go: Plugin failed with status code 1.
```

**Cause**: The Go Protocol Buffer compiler plugin is not installed.

**Solution**:
```bash
# Install Go protobuf plugins
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Verify installation
protoc-gen-go --version

# Ensure GOPATH/bin is in PATH
# Windows:
set PATH=%PATH%;%USERPROFILE%\go\bin

# Linux/Mac:
export PATH=$PATH:$(go env GOPATH)/bin
```

**Add to go.mod**:
```go
require (
    google.golang.org/protobuf v1.32.0
    google.golang.org/grpc v1.60.0
)
```

---

### Issue 3: JavaScript Protobuf Plugin Missing

**Error**:
```
'protoc-gen-js' is not recognized as an internal or external command
--js_out: protoc-gen-js: Plugin failed with status code 1.
```

**Cause**: The JavaScript Protocol Buffer compiler plugin is not installed.

**Solution**:
```bash
# Option 1: Install globally
npm install -g protoc-gen-js

# Option 2: Use google-protobuf (already in package.json)
# The project uses google-protobuf which includes the plugin

# Verify installation
protoc-gen-js --version

# Alternative: Use protoc-gen-grpc-web for modern JS
npm install -g protoc-gen-grpc-web
```

---

## 2. Complete Setup Instructions

### Prerequisites

1. **Protocol Buffer Compiler (protoc)**
   ```bash
   # Windows: Download from GitHub releases
   # https://github.com/protocolbuffers/protobuf/releases
   # Extract and add to PATH
   
   # Linux:
   sudo apt-get install protobuf-compiler
   
   # Mac:
   brew install protobuf
   
   # Verify:
   protoc --version  # Should show libprotoc 3.x or 4.x
   ```

2. **Python 3.9+**
   ```bash
   python --version  # Should be 3.9 or higher
   ```

3. **Node.js 18+**
   ```bash
   node --version  # Should be 18.x or higher
   ```

4. **Go 1.21+**
   ```bash
   go version  # Should be 1.21 or higher
   ```

### Step-by-Step Setup

#### Step 1: Install Protocol Buffer Compiler

**Windows**:
```powershell
# Download protoc from GitHub
# https://github.com/protocolbuffers/protobuf/releases/latest
# Example: protoc-25.1-win64.zip

# Extract to C:\protoc
# Add to PATH:
$env:PATH += ";C:\protoc\bin"

# Verify
protoc --version
```

**Linux**:
```bash
sudo apt-get update
sudo apt-get install -y protobuf-compiler
protoc --version
```

**Mac**:
```bash
brew install protobuf
protoc --version
```

#### Step 2: Install Python Dependencies

```bash
cd empath-engine

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
cd services/emotion-inference
pip install -r requirements.txt
pip install grpcio-tools  # CRITICAL: Missing from requirements.txt

cd ../character-memory
pip install -r requirements.txt
pip install grpcio-tools  # CRITICAL: Missing from requirements.txt
```

#### Step 3: Install Go Dependencies

```bash
cd empath-engine/services/llm-gateway

# Download dependencies
go mod download

# Install protobuf plugins
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Add GOPATH/bin to PATH if not already
# Windows:
set PATH=%PATH%;%USERPROFILE%\go\bin
# Linux/Mac:
export PATH=$PATH:$(go env GOPATH)/bin

# Verify
protoc-gen-go --version
```

#### Step 4: Install Node.js Dependencies

```bash
cd empath-engine/services/narrative-director

# Install dependencies
npm install

# Install protobuf plugin globally
npm install -g protoc-gen-js

# Or install locally
npm install --save-dev protoc-gen-js
```

#### Step 5: Generate Protocol Buffer Code

```bash
cd empath-engine

# Run the generation script
make generate-proto

# Or manually:
cd shared/proto
protoc --python_out=../../services/emotion-inference/proto \
       --go_out=../../services/llm-gateway/pkg/proto \
       --js_out=import_style=commonjs:../../services/narrative-director/src/proto \
       emotion.proto
```

#### Step 6: Verify Setup

```bash
# Check if proto files were generated
ls services/emotion-inference/proto/emotion_pb2.py
ls services/llm-gateway/pkg/proto/emotion.pb.go
ls services/narrative-director/src/proto/emotion_pb.js

# If all files exist, setup is complete!
```

---

## 3. Common Issues & Solutions

### Issue: "protoc: command not found"

**Solution**:
```bash
# Verify protoc is installed
which protoc  # Linux/Mac
where protoc  # Windows

# If not found, install protoc (see Step 1)
# Ensure it's in your PATH
```

### Issue: "ModuleNotFoundError: No module named 'proto'"

**Solution**:
```bash
# The proto directory might not be in Python path
# Add __init__.py to proto directory
cd services/emotion-inference/proto
touch __init__.py  # Linux/Mac
type nul > __init__.py  # Windows

# Or run from correct directory
cd services/emotion-inference
python -m src.main
```

### Issue: "cannot find package empathengine/llm-gateway/pkg/proto"

**Solution**:
```bash
# Regenerate Go proto files
cd empath-engine
make generate-proto

# Or manually:
cd shared/proto
protoc --go_out=../../services/llm-gateway/pkg/proto \
       --go_opt=paths=source_relative \
       emotion.proto
```

### Issue: "Cannot find module './proto/emotion_pb.js'"

**Solution**:
```bash
# Regenerate JavaScript proto files
cd empath-engine
make generate-proto

# Or manually:
cd shared/proto
protoc --js_out=import_style=commonjs:../../services/narrative-director/src/proto \
       emotion.proto
```

### Issue: "go: cannot find main module"

**Solution**:
```bash
# Initialize Go module if missing
cd services/llm-gateway
go mod init empathengine/llm-gateway
go mod tidy
```

### Issue: Python version mismatch (using Python 3.9 instead of 3.11+)

**Observation**: The log shows Python 3.9 is being used, but the code uses Python 3.11+ syntax (`int | None`).

**Solution**:
```bash
# Option 1: Upgrade Python
# Download Python 3.11+ from python.org

# Option 2: Use Python 3.9 compatible syntax
# Change: int | None
# To: Optional[int]
from typing import Optional

# Option 3: Use pyenv to manage Python versions
pyenv install 3.11
pyenv local 3.11
```

---

## 4. Updated Makefile

The current Makefile has issues. Here's an improved version:

```makefile
.PHONY: init generate-proto build-services test-all clean

# Initialize project
init: check-tools install-deps generate-proto
	@echo "✅ Project initialized successfully"

# Check required tools
check-tools:
	@echo "Checking required tools..."
	@command -v protoc >/dev/null 2>&1 || { echo "❌ protoc not found. Install Protocol Buffers compiler."; exit 1; }
	@command -v python >/dev/null 2>&1 || { echo "❌ python not found."; exit 1; }
	@command -v node >/dev/null 2>&1 || { echo "❌ node not found."; exit 1; }
	@command -v go >/dev/null 2>&1 || { echo "❌ go not found."; exit 1; }
	@echo "✅ All required tools found"

# Install dependencies
install-deps:
	@echo "Installing Python dependencies..."
	cd services/emotion-inference && pip install -r requirements.txt && pip install grpcio-tools
	cd services/character-memory && pip install -r requirements.txt && pip install grpcio-tools
	@echo "Installing Node.js dependencies..."
	cd services/narrative-director && npm install
	@echo "Installing Go dependencies..."
	cd services/llm-gateway && go mod download
	@echo "Installing protobuf plugins..."
	go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
	npm install -g protoc-gen-js || echo "Warning: protoc-gen-js installation failed"

# Generate Protocol Buffer code
generate-proto:
	@echo "Generating Protocol Buffer code..."
	@mkdir -p services/emotion-inference/proto
	@mkdir -p services/llm-gateway/pkg/proto
	@mkdir -p services/narrative-director/src/proto
	cd shared/proto && protoc --python_out=../../services/emotion-inference/proto \
		--go_out=../../services/llm-gateway/pkg/proto \
		--go_opt=paths=source_relative \
		--js_out=import_style=commonjs:../../services/narrative-director/src/proto \
		emotion.proto
	@echo "✅ Protocol Buffer code generated"

# Build all services
build-services:
	@echo "Building services..."
	cd services/llm-gateway && go build -o bin/llm-gateway cmd/main.go
	@echo "✅ Services built"

# Run tests
test-all:
	@echo "Running tests..."
	cd services/emotion-inference && pytest tests/
	cd services/narrative-director && npm test
	cd services/llm-gateway && go test ./...
	@echo "✅ All tests passed"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -rf services/emotion-inference/proto/*
	rm -rf services/llm-gateway/pkg/proto/*
	rm -rf services/narrative-director/src/proto/*
	rm -rf services/llm-gateway/bin/*
	@echo "✅ Cleaned"
```

---

## 5. Updated Requirements Files

### services/emotion-inference/requirements.txt

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
protobuf==4.25.3
pytest==7.4.3
grpcio-tools==1.60.0  # ADDED: Required for protobuf generation
```

### services/character-memory/requirements.txt

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
grpcio-tools==1.60.0  # ADDED: Required for protobuf generation
```

### services/llm-gateway/go.mod

```go
module empathengine/llm-gateway

go 1.21

require (
    google.golang.org/protobuf v1.32.0
    google.golang.org/grpc v1.60.0
)
```

---

## 6. Verification Checklist

After setup, verify everything works:

- [ ] `protoc --version` shows version 3.x or 4.x
- [ ] `python --version` shows 3.11 or higher (or code updated for 3.9)
- [ ] `node --version` shows 18.x or higher
- [ ] `go version` shows 1.21 or higher
- [ ] `protoc-gen-go --version` works
- [ ] `protoc-gen-js --version` works (or installed locally)
- [ ] `python -m grpc_tools.protoc --version` works
- [ ] `make generate-proto` completes without errors
- [ ] Generated proto files exist in all services
- [ ] `make build-services` completes without errors
- [ ] `make test-all` passes (or runs without import errors)

---

## 7. Docker Setup (Alternative)

If local setup is too complex, use Docker:

```bash
# Build all services
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Note**: Docker setup should handle protobuf generation automatically in the Dockerfiles.

---

## 8. Recommended Development Environment

### VS Code Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "dbaeumer.vscode-eslint",
    "golang.go",
    "zxh404.vscode-proto3",
    "ms-azuretools.vscode-docker"
  ]
}
```

### Python Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install all dependencies
pip install -r services/emotion-inference/requirements.txt
pip install -r services/character-memory/requirements.txt
pip install grpcio-tools
```

---

## 9. Next Steps After Setup

Once setup is complete:

1. **Verify Services Start**:
   ```bash
   # Terminal 1: Emotion Inference
   cd services/emotion-inference
   uvicorn src.main:app --reload --port 8000
   
   # Terminal 2: Narrative Director
   cd services/narrative-director
   npm start
   
   # Terminal 3: LLM Gateway
   cd services/llm-gateway
   go run cmd/main.go
   
   # Terminal 4: Character Memory
   cd services/character-memory
   uvicorn src.main:app --reload --port 8001
   ```

2. **Test Endpoints**:
   ```bash
   # Health checks
   curl http://localhost:8000/health
   curl http://localhost:3000/health
   curl http://localhost:8080/health
   curl http://localhost:8001/health
   ```

3. **Run Tests**:
   ```bash
   make test-all
   ```

4. **Start Development**:
   - Review PROJECT_ANALYSIS.md for code quality issues
   - Implement authentication
   - Replace mock responses with real logic
   - Increase test coverage

---

## 10. Support & Resources

### Official Documentation
- Protocol Buffers: https://protobuf.dev/
- FastAPI: https://fastapi.tiangolo.com/
- Express.js: https://expressjs.com/
- Go: https://go.dev/doc/

### Troubleshooting
- Check `Protobuf.txt` for build logs
- Review `PROJECT_ANALYSIS.md` for code issues
- See `DEPLOYMENT.md` for deployment guides

### Getting Help
- Open an issue on GitHub
- Check existing documentation in `/docs`
- Review error logs in service directories

---

**Status After Following This Guide**: ✅ **Ready for Development**

**Estimated Setup Time**: 30-60 minutes (depending on download speeds)
