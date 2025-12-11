# Quick Reference Guide

## Essential Commands

### Project Setup

```bash
# Clone repository
git clone https://github.com/yourusername/empath-engine.git
cd empath-engine

# Initialize project (install dependencies, generate proto)
make init

# Start all services
make dev-up

# Stop all services
make dev-down
```

### Service Management

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f emotion-inference

# Scale services
docker-compose up -d --scale emotion-inference=3
```

### Health Checks

```bash
# Check all services
curl http://localhost:8000/health  # Emotion Inference
curl http://localhost:3000/health  # Narrative Director
curl http://localhost:8080/health  # LLM Gateway
curl http://localhost:8001/health  # Character Memory

# Check Redis
docker-compose exec redis redis-cli ping
```

### Building

```bash
# Build all services
make build-services

# Build individual services
make build-emotion
make build-narrative
make build-llm
make build-character

# Docker build
docker-compose build
docker-compose build --no-cache
```

### Testing

```bash
# Test emotion inference
make test-emotion

# Python tests
cd services/emotion-inference
pytest tests/ -v

# Node.js tests
cd services/narrative-director
npm test

# Go tests
cd services/llm-gateway
go test ./... -v
```

### Development

```bash
# Generate Protocol Buffers
make generate-proto

# Run service locally (Python)
cd services/emotion-inference
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload

# Run service locally (Node.js)
cd services/narrative-director
npm install
npm start

# Run service locally (Go)
cd services/llm-gateway
go run cmd/main.go
```

## API Quick Reference

### Emotion Inference

```bash
# Infer emotion
curl -X POST http://localhost:8000/infer \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user-123",
    "timestamp_ms": 1704067200000,
    "decision_latency_ms": 1250.5,
    "action_frequency": 15,
    "recent_choices": [1, 2, 1, 3, 2],
    "context_data": {"difficulty": 0.75}
  }'
```

### Narrative Director

```bash
# Generate narrative
curl -X POST http://localhost:3000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "emotion_data": {
      "dominant_emotion": "focused",
      "confidence": 0.87
    },
    "context": {
      "scene_id": "chapter1-scene3"
    }
  }'
```

### LLM Gateway

```bash
# Complete request
curl -X POST http://localhost:8080/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Generate a supportive message",
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

### Character Memory

```bash
# Get character memory
curl "http://localhost:8001/memory?character_id=npc-001&session_id=user-123"
```

## Docker Commands

### Container Management

```bash
# List containers
docker-compose ps

# Execute command in container
docker-compose exec emotion-inference /bin/bash

# View container stats
docker stats

# Remove all containers
docker-compose down -v
```

### Image Management

```bash
# List images
docker images

# Remove unused images
docker image prune

# Tag image
docker tag emotion-inference:latest myregistry/emotion-inference:v1.0

# Push image
docker push myregistry/emotion-inference:v1.0
```

### Volume Management

```bash
# List volumes
docker volume ls

# Remove unused volumes
docker volume prune

# Inspect volume
docker volume inspect empath-engine_redis-data
```

## Kubernetes Commands

### Deployment

```bash
# Create namespace
kubectl create namespace empath-engine

# Apply configurations
kubectl apply -f k8s/

# Delete resources
kubectl delete -f k8s/
```

### Pod Management

```bash
# List pods
kubectl get pods -n empath-engine

# Describe pod
kubectl describe pod <pod-name> -n empath-engine

# View logs
kubectl logs -f <pod-name> -n empath-engine

# Execute command in pod
kubectl exec -it <pod-name> -n empath-engine -- /bin/bash
```

### Service Management

```bash
# List services
kubectl get services -n empath-engine

# Describe service
kubectl describe service emotion-inference -n empath-engine

# Port forward
kubectl port-forward service/emotion-inference 8000:8000 -n empath-engine
```

### Scaling

```bash
# Scale deployment
kubectl scale deployment emotion-inference --replicas=5 -n empath-engine

# Autoscale
kubectl autoscale deployment emotion-inference --min=2 --max=10 --cpu-percent=80 -n empath-engine
```

### Rollout Management

```bash
# Check rollout status
kubectl rollout status deployment/emotion-inference -n empath-engine

# View rollout history
kubectl rollout history deployment/emotion-inference -n empath-engine

# Rollback
kubectl rollout undo deployment/emotion-inference -n empath-engine
```

## Git Workflow

### Branch Management

```bash
# Create feature branch
git checkout -b feature/your-feature

# Switch branches
git checkout main

# List branches
git branch -a

# Delete branch
git branch -d feature/your-feature
```

### Committing

```bash
# Stage changes
git add .

# Commit with message
git commit -m "feat: add new feature"

# Amend last commit
git commit --amend
```

### Syncing

```bash
# Fetch updates
git fetch upstream

# Rebase on main
git rebase upstream/main

# Push changes
git push origin feature/your-feature

# Force push (after rebase)
git push origin feature/your-feature --force-with-lease
```

## Debugging

### View Logs

```bash
# Docker Compose
docker-compose logs -f --tail=100 emotion-inference

# Kubernetes
kubectl logs -f deployment/emotion-inference -n empath-engine
```

### Check Service Status

```bash
# Docker
docker-compose ps

# Kubernetes
kubectl get pods -n empath-engine
```

### Network Debugging

```bash
# Test connectivity
docker-compose exec emotion-inference curl http://redis:6379

# Inspect network
docker network inspect empath-engine_default
```

### Resource Usage

```bash
# Docker stats
docker stats

# Kubernetes resource usage
kubectl top pods -n empath-engine
kubectl top nodes
```

## Redis Commands

### Connect to Redis

```bash
# Docker Compose
docker-compose exec redis redis-cli

# Kubernetes
kubectl exec -it redis-0 -n empath-engine -- redis-cli
```

### Common Operations

```bash
# Ping
PING

# Get all keys
KEYS *

# Get value
GET key_name

# Set value
SET key_name value

# Delete key
DEL key_name

# Flush all data
FLUSHALL

# Get info
INFO

# Monitor commands
MONITOR
```

## Environment Variables

### Set Environment Variables

```bash
# Linux/Mac
export REDIS_HOST=localhost
export REDIS_PORT=6379

# Windows (PowerShell)
$env:REDIS_HOST="localhost"
$env:REDIS_PORT="6379"

# Windows (CMD)
set REDIS_HOST=localhost
set REDIS_PORT=6379
```

### Load from .env File

```bash
# Create .env file
cat > .env << EOF
REDIS_HOST=redis
REDIS_PORT=6379
LOG_LEVEL=INFO
EOF

# Load in Docker Compose (automatic)
docker-compose up -d
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

### Permission Denied

```bash
# Fix file permissions
chmod +x scripts/generate-proto.sh

# Run with sudo (if needed)
sudo docker-compose up -d
```

### Out of Memory

```bash
# Increase Docker memory limit
# Docker Desktop → Settings → Resources → Memory

# Clear Docker cache
docker system prune -a
```

### Service Won't Start

```bash
# Check logs
docker-compose logs emotion-inference

# Rebuild container
docker-compose build --no-cache emotion-inference
docker-compose up -d emotion-inference
```

## Performance Monitoring

### Check Response Times

```bash
# Using curl
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# curl-format.txt content:
time_namelookup:  %{time_namelookup}\n
time_connect:  %{time_connect}\n
time_starttransfer:  %{time_starttransfer}\n
time_total:  %{time_total}\n
```

### Load Testing

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/health

# Using wrk
wrk -t12 -c400 -d30s http://localhost:8000/health
```

## Backup and Restore

### Backup Redis

```bash
# Create backup
docker-compose exec redis redis-cli BGSAVE
docker cp empath-engine_redis_1:/data/dump.rdb ./backup/

# Kubernetes
kubectl exec redis-0 -n empath-engine -- redis-cli BGSAVE
kubectl cp empath-engine/redis-0:/data/dump.rdb ./backup/dump.rdb
```

### Restore Redis

```bash
# Restore backup
docker cp ./backup/dump.rdb empath-engine_redis_1:/data/
docker-compose restart redis

# Kubernetes
kubectl cp ./backup/dump.rdb empath-engine/redis-0:/data/dump.rdb
kubectl delete pod redis-0 -n empath-engine
```

## Useful Aliases

Add to your `.bashrc` or `.zshrc`:

```bash
# Docker Compose shortcuts
alias dc='docker-compose'
alias dcu='docker-compose up -d'
alias dcd='docker-compose down'
alias dcl='docker-compose logs -f'
alias dcp='docker-compose ps'

# Kubernetes shortcuts
alias k='kubectl'
alias kgp='kubectl get pods -n empath-engine'
alias kgs='kubectl get services -n empath-engine'
alias kl='kubectl logs -f -n empath-engine'

# Empath Engine specific
alias ee-up='cd ~/empath-engine && make dev-up'
alias ee-down='cd ~/empath-engine && make dev-down'
alias ee-logs='cd ~/empath-engine && docker-compose logs -f'
```

## Quick Links

- **Documentation**: [DOCS_INDEX.md](DOCS_INDEX.md)
- **API Reference**: [API.md](API.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Need more help?** Check the full documentation or open an issue on GitHub.
