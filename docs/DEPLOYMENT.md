# Deployment Guide

## Overview

This guide covers deployment strategies for Empath Engine across different environments, from local development to production Kubernetes clusters.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Environment Configuration](#environment-configuration)
- [Monitoring and Logging](#monitoring-and-logging)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Docker**: v20.10 or higher
- **Docker Compose**: v2.0 or higher
- **Make**: For build automation
- **Git**: For version control

### Optional (for production)

- **Kubernetes**: v1.24 or higher
- **kubectl**: Kubernetes CLI
- **Helm**: v3.0 or higher (for Kubernetes deployments)

## Local Development

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/empath-engine.git
   cd empath-engine
   ```

2. **Initialize the project**:
   ```bash
   make init
   ```

3. **Start all services**:
   ```bash
   make dev-up
   ```

4. **Verify services are running**:
   ```bash
   curl http://localhost:8000/health  # Emotion Inference
   curl http://localhost:3000/health  # Narrative Director
   curl http://localhost:8080/health  # LLM Gateway
   curl http://localhost:8001/health  # Character Memory
   ```

5. **Stop services**:
   ```bash
   make dev-down
   ```

### Running Individual Services

#### Emotion Inference Service

```bash
cd services/emotion-inference
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### Narrative Director Service

```bash
cd services/narrative-director
npm install
npm start
```

#### LLM Gateway Service

```bash
cd services/llm-gateway
go mod download
go run cmd/main.go
```

#### Character Memory Service

```bash
cd services/character-memory
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
```

## Docker Deployment

### Using Docker Compose

#### Development Mode

```bash
docker-compose up -d
```

This starts all services with:
- Hot reloading enabled
- Debug logging
- Development dependencies

#### Production Mode

Create a `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes

  emotion-inference:
    build:
      context: ./services/emotion-inference
      dockerfile: Dockerfile
    restart: always
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - LOG_LEVEL=INFO
    depends_on:
      - redis
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 512M

  narrative-director:
    build:
      context: ./services/narrative-director
      dockerfile: Dockerfile
    restart: always
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - NODE_ENV=production
    depends_on:
      - redis
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 256M

  llm-gateway:
    build:
      context: ./services/llm-gateway
      dockerfile: Dockerfile
    restart: always
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 256M

  character-memory:
    build:
      context: ./services/character-memory
      dockerfile: Dockerfile
    restart: always
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - LOG_LEVEL=INFO
    depends_on:
      - redis
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 256M

volumes:
  redis-data:
```

Deploy with:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Building Images

#### Build all services:

```bash
docker-compose build
```

#### Build specific service:

```bash
docker-compose build emotion-inference
```

#### Build with no cache:

```bash
docker-compose build --no-cache
```

### Scaling Services

```bash
docker-compose up -d --scale emotion-inference=3
docker-compose up -d --scale narrative-director=2
```

### Viewing Logs

```bash
docker-compose logs -f                    # All services
docker-compose logs -f emotion-inference  # Specific service
docker-compose logs --tail=100 -f         # Last 100 lines
```

## Production Deployment

### Kubernetes Deployment

#### Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl configured
- Helm 3 installed

#### 1. Create Namespace

```bash
kubectl create namespace empath-engine
```

#### 2. Deploy Redis

Create `k8s/redis-deployment.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: empath-engine
spec:
  ports:
    - port: 6379
      targetPort: 6379
  selector:
    app: redis
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: empath-engine
spec:
  serviceName: redis
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: redis:7-alpine
          ports:
            - containerPort: 6379
          volumeMounts:
            - name: redis-data
              mountPath: /data
  volumeClaimTemplates:
    - metadata:
        name: redis-data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
```

Deploy:

```bash
kubectl apply -f k8s/redis-deployment.yaml
```

#### 3. Deploy Services

Create `k8s/emotion-inference-deployment.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: emotion-inference
  namespace: empath-engine
spec:
  type: ClusterIP
  ports:
    - port: 8000
      targetPort: 8000
  selector:
    app: emotion-inference
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: emotion-inference
  namespace: empath-engine
spec:
  replicas: 3
  selector:
    matchLabels:
      app: emotion-inference
  template:
    metadata:
      labels:
        app: emotion-inference
    spec:
      containers:
        - name: emotion-inference
          image: your-registry/emotion-inference:latest
          ports:
            - containerPort: 8000
          env:
            - name: REDIS_HOST
              value: redis
            - name: REDIS_PORT
              value: "6379"
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 5
```

Deploy all services:

```bash
kubectl apply -f k8s/emotion-inference-deployment.yaml
kubectl apply -f k8s/narrative-director-deployment.yaml
kubectl apply -f k8s/llm-gateway-deployment.yaml
kubectl apply -f k8s/character-memory-deployment.yaml
```

#### 4. Configure Ingress

Create `k8s/ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: empath-engine-ingress
  namespace: empath-engine
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: api.empathengine.io
      http:
        paths:
          - path: /emotion
            pathType: Prefix
            backend:
              service:
                name: emotion-inference
                port:
                  number: 8000
          - path: /narrative
            pathType: Prefix
            backend:
              service:
                name: narrative-director
                port:
                  number: 3000
          - path: /llm
            pathType: Prefix
            backend:
              service:
                name: llm-gateway
                port:
                  number: 8080
          - path: /memory
            pathType: Prefix
            backend:
              service:
                name: character-memory
                port:
                  number: 8001
```

Deploy:

```bash
kubectl apply -f k8s/ingress.yaml
```

#### 5. Verify Deployment

```bash
kubectl get pods -n empath-engine
kubectl get services -n empath-engine
kubectl get ingress -n empath-engine
```

### Helm Chart (Recommended)

Create a Helm chart for easier management:

```bash
helm create empath-engine
```

Install:

```bash
helm install empath-engine ./empath-engine -n empath-engine
```

Upgrade:

```bash
helm upgrade empath-engine ./empath-engine -n empath-engine
```

## Environment Configuration

### Environment Variables

#### Emotion Inference Service

```env
REDIS_HOST=redis
REDIS_PORT=6379
LOG_LEVEL=INFO
MODEL_PATH=/models/emotion_model.pkl
CACHE_TTL=300
```

#### Narrative Director Service

```env
REDIS_HOST=redis
REDIS_PORT=6379
NODE_ENV=production
LLM_GATEWAY_URL=http://llm-gateway:8080
PORT=3000
```

#### LLM Gateway Service

```env
REDIS_HOST=redis
REDIS_PORT=6379
OPENAI_API_KEY=your-api-key
ANTHROPIC_API_KEY=your-api-key
DEFAULT_PROVIDER=openai
CACHE_ENABLED=true
```

#### Character Memory Service

```env
REDIS_HOST=redis
REDIS_PORT=6379
LOG_LEVEL=INFO
MEMORY_TTL=86400
```

### Secrets Management

#### Using Kubernetes Secrets

```bash
kubectl create secret generic llm-api-keys \
  --from-literal=openai-key=your-openai-key \
  --from-literal=anthropic-key=your-anthropic-key \
  -n empath-engine
```

Reference in deployment:

```yaml
env:
  - name: OPENAI_API_KEY
    valueFrom:
      secretKeyRef:
        name: llm-api-keys
        key: openai-key
```

## Monitoring and Logging

### Health Checks

All services expose health endpoints:

```bash
curl http://localhost:8000/health  # Emotion Inference
curl http://localhost:3000/health  # Narrative Director
curl http://localhost:8080/health  # LLM Gateway
curl http://localhost:8001/health  # Character Memory
```

### Logging

#### Docker Compose

```bash
docker-compose logs -f --tail=100
```

#### Kubernetes

```bash
kubectl logs -f deployment/emotion-inference -n empath-engine
kubectl logs -f -l app=emotion-inference -n empath-engine --all-containers
```

### Metrics (Future)

Prometheus metrics will be exposed at `/metrics` endpoint.

## Troubleshooting

### Common Issues

#### Services Not Starting

**Check logs**:
```bash
docker-compose logs emotion-inference
```

**Verify dependencies**:
```bash
docker-compose ps
```

#### Connection Refused

**Check Redis**:
```bash
docker-compose exec redis redis-cli ping
```

**Verify network**:
```bash
docker network ls
docker network inspect empath-engine_default
```

#### High Memory Usage

**Check resource usage**:
```bash
docker stats
```

**Adjust limits in docker-compose.yml**:
```yaml
deploy:
  resources:
    limits:
      memory: 512M
```

#### Port Conflicts

**Change ports in docker-compose.yml**:
```yaml
ports:
  - "8001:8000"  # Host:Container
```

### Debugging

#### Access container shell:

```bash
docker-compose exec emotion-inference /bin/bash
```

#### View environment variables:

```bash
docker-compose exec emotion-inference env
```

#### Test service connectivity:

```bash
docker-compose exec emotion-inference curl http://redis:6379
```

## Backup and Recovery

### Redis Backup

```bash
docker-compose exec redis redis-cli BGSAVE
docker cp empath-engine_redis_1:/data/dump.rdb ./backup/
```

### Restore Redis

```bash
docker cp ./backup/dump.rdb empath-engine_redis_1:/data/
docker-compose restart redis
```

## Security Best Practices

1. **Use secrets management** for API keys
2. **Enable TLS/SSL** for production
3. **Implement rate limiting** at API gateway
4. **Regular security updates** for base images
5. **Network policies** in Kubernetes
6. **RBAC** for Kubernetes access

## Performance Tuning

### Redis Optimization

```bash
# Increase max memory
redis-cli CONFIG SET maxmemory 2gb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### Service Scaling

```bash
# Scale based on load
kubectl scale deployment emotion-inference --replicas=5 -n empath-engine
```

### Resource Limits

Adjust based on monitoring:

```yaml
resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 2000m
    memory: 1Gi
```

## Rollback Procedures

### Docker Compose

```bash
git checkout previous-version
docker-compose down
docker-compose up -d
```

### Kubernetes

```bash
kubectl rollout undo deployment/emotion-inference -n empath-engine
kubectl rollout status deployment/emotion-inference -n empath-engine
```

### Helm

```bash
helm rollback empath-engine 1 -n empath-engine
```

## Support

For deployment issues:
- GitHub Issues: [Report a problem](https://github.com/yourusername/empath-engine/issues)
- Documentation: [Full docs](https://docs.empathengine.io)
- Email: devops@synapticneurogaming.com

---

**Last Updated**: January 2025  
**Version**: 1.0.0
