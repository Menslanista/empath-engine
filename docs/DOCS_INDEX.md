# Empath Engine Documentation

Welcome to the Empath Engine documentation! This index provides quick access to all documentation resources.

## 📚 Documentation Structure

### Getting Started

- **[README.md](README.md)** - Project overview, quick start guide, and basic usage
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes
- **[LICENSE](LICENSE)** - MIT License terms

### Development

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributing to the project
  - Code of conduct
  - Development workflow
  - Coding standards (Python, JavaScript, Go)
  - Testing guidelines
  - Pull request process

### Technical Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design
  - Microservices overview
  - Service responsibilities
  - Communication patterns
  - Data models
  - Security architecture
  - Performance optimization

- **[API.md](API.md)** - Complete API reference
  - Emotion Inference API
  - Narrative Director API
  - LLM Gateway API
  - Character Memory API
  - Error handling
  - Rate limiting

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment instructions
  - Local development setup
  - Docker deployment
  - Kubernetes deployment
  - Environment configuration
  - Monitoring and logging
  - Troubleshooting

## 🚀 Quick Links

### For New Users

1. Start with [README.md](README.md) for project overview
2. Follow the [Quick Start](README.md#quick-start) guide
3. Explore the [API Documentation](API.md)

### For Developers

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
3. Check [Coding Standards](CONTRIBUTING.md#coding-standards)

### For DevOps

1. Follow [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions
2. Review [Environment Configuration](DEPLOYMENT.md#environment-configuration)
3. Set up [Monitoring and Logging](DEPLOYMENT.md#monitoring-and-logging)

## 📖 Documentation by Topic

### Architecture & Design

- [System Overview](ARCHITECTURE.md#system-overview)
- [Design Principles](ARCHITECTURE.md#design-principles)
- [Service Details](ARCHITECTURE.md#service-details)
- [Communication Patterns](ARCHITECTURE.md#communication-patterns)
- [Data Models](ARCHITECTURE.md#data-models)

### API Reference

- [Emotion Inference Service](API.md#emotion-inference-service)
- [Narrative Director Service](API.md#narrative-director-service)
- [LLM Gateway Service](API.md#llm-gateway-service)
- [Character Memory Service](API.md#character-memory-service)
- [Error Responses](API.md#error-responses)

### Development

- [Project Structure](README.md#project-structure)
- [Local Development](DEPLOYMENT.md#local-development)
- [Testing](README.md#testing)
- [Protocol Buffers](README.md#protocol-buffer-definitions)

### Deployment

- [Docker Deployment](DEPLOYMENT.md#docker-deployment)
- [Kubernetes Deployment](DEPLOYMENT.md#kubernetes-deployment)
- [Environment Variables](DEPLOYMENT.md#environment-configuration)
- [Scaling Services](DEPLOYMENT.md#scaling-services)

### Operations

- [Monitoring](DEPLOYMENT.md#monitoring-and-logging)
- [Troubleshooting](DEPLOYMENT.md#troubleshooting)
- [Backup and Recovery](DEPLOYMENT.md#backup-and-recovery)
- [Security Best Practices](DEPLOYMENT.md#security-best-practices)

## 🔍 Search by Service

### Emotion Inference Service (Python/FastAPI)

- [Service Overview](ARCHITECTURE.md#1-emotion-inference-service)
- [API Endpoints](API.md#emotion-inference-service)
- [Local Development](DEPLOYMENT.md#emotion-inference-service)
- [Dockerfile](services/emotion-inference/Dockerfile)

### Narrative Director Service (Node.js/Express)

- [Service Overview](ARCHITECTURE.md#2-narrative-director-service)
- [API Endpoints](API.md#narrative-director-service)
- [Local Development](DEPLOYMENT.md#narrative-director-service)
- [Dockerfile](services/narrative-director/Dockerfile)

### LLM Gateway Service (Go)

- [Service Overview](ARCHITECTURE.md#3-llm-gateway-service)
- [API Endpoints](API.md#llm-gateway-service)
- [Local Development](DEPLOYMENT.md#llm-gateway-service)
- [Dockerfile](services/llm-gateway/Dockerfile)

### Character Memory Service (Python/FastAPI)

- [Service Overview](ARCHITECTURE.md#4-character-memory-service)
- [API Endpoints](API.md#character-memory-service)
- [Local Development](DEPLOYMENT.md#character-memory-service)
- [Dockerfile](services/character-memory/Dockerfile)

## 🛠️ Common Tasks

### Setup and Installation

```bash
# Clone repository
git clone https://github.com/yourusername/empath-engine.git
cd empath-engine

# Initialize project
make init

# Start services
make dev-up
```

See: [Installation Guide](README.md#installation)

### Making Changes

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes and test
make test-emotion

# Commit and push
git commit -m "feat: your feature"
git push origin feature/your-feature
```

See: [Development Workflow](CONTRIBUTING.md#development-workflow)

### Deploying

```bash
# Docker Compose
docker-compose up -d

# Kubernetes
kubectl apply -f k8s/
```

See: [Deployment Guide](DEPLOYMENT.md)

## 📊 Diagrams

### System Architecture

```
Client → API Gateway → Services → Redis
```

See: [Architecture Diagram](ARCHITECTURE.md#system-architecture)

### Data Flow

```
Player Action → Emotion Inference → Narrative Director → Response
```

See: [Data Flow](ARCHITECTURE.md#data-flow)

## 🔗 External Resources

### Official Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Express.js Documentation](https://expressjs.com/)
- [Go Documentation](https://go.dev/doc/)
- [Redis Documentation](https://redis.io/documentation)
- [Protocol Buffers](https://protobuf.dev/)

### Community

- [GitHub Repository](https://github.com/yourusername/empath-engine)
- [GitHub Issues](https://github.com/yourusername/empath-engine/issues)
- [GitHub Discussions](https://github.com/yourusername/empath-engine/discussions)

### Support

- **Email**: support@synapticneurogaming.com
- **Documentation**: https://docs.empathengine.io
- **API Status**: https://status.empathengine.io

## 📝 Documentation Standards

### Writing Guidelines

- Use clear, concise language
- Include code examples
- Provide context and explanations
- Keep documentation up-to-date
- Follow Markdown best practices

### Contributing to Documentation

1. Documentation changes follow the same PR process as code
2. Update relevant sections when adding features
3. Include examples and use cases
4. Test all code snippets
5. Update the changelog

See: [Contributing Guidelines](CONTRIBUTING.md)

## 🔄 Documentation Updates

This documentation is actively maintained. Last updated: **January 2025**

To report documentation issues:
- Open an [issue](https://github.com/yourusername/empath-engine/issues)
- Submit a [pull request](https://github.com/yourusername/empath-engine/pulls)
- Contact us at docs@synapticneurogaming.com

## 📜 Version Information

- **Documentation Version**: 1.0.0
- **Project Version**: 0.1.0
- **Last Updated**: January 2025

---

**Need help?** Check our [FAQ](README.md#support) or reach out to the community!
