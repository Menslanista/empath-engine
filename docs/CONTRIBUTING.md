# Contributing to Empath Engine

Thank you for your interest in contributing to Empath Engine! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

### Our Pledge

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior:
- The use of sexualized language or imagery and unwelcome sexual attention
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

## Getting Started

### Prerequisites

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/empath-engine.git
   cd empath-engine
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/original/empath-engine.git
   ```
4. Install dependencies:
   ```bash
   make init
   ```

### Setting Up Your Development Environment

1. **Python Services** (Emotion Inference, Character Memory):
   ```bash
   cd services/emotion-inference
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

2. **Node.js Service** (Narrative Director):
   ```bash
   cd services/narrative-director
   npm install
   ```

3. **Go Service** (LLM Gateway):
   ```bash
   cd services/llm-gateway
   go mod download
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications

### 2. Make Your Changes

- Write clean, maintainable code
- Follow the coding standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Your Changes

Use conventional commit messages:

```bash
git commit -m "feat: add emotion caching mechanism"
git commit -m "fix: resolve race condition in narrative director"
git commit -m "docs: update API documentation"
git commit -m "test: add unit tests for emotion inference"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### 4. Keep Your Branch Updated

```bash
git fetch upstream
git rebase upstream/main
```

### 5. Push Your Changes

```bash
git push origin feature/your-feature-name
```

## Coding Standards

### Python (Emotion Inference, Character Memory)

- Follow **PEP 8** style guide
- Use **type hints** for all function signatures
- Maximum line length: **88 characters** (Black formatter)
- Use **docstrings** for all public functions and classes

Example:
```python
from typing import Dict, Optional

async def infer_emotion(
    data: PlayerBehaviorData,
    context: Optional[Dict[str, float]] = None
) -> EmotionPrediction:
    """
    Infer emotion from player behavioral data.
    
    Args:
        data: Player behavior data containing session and action info
        context: Optional contextual data for enhanced inference
        
    Returns:
        EmotionPrediction with dominant emotion and confidence scores
    """
    pass
```

**Tools**:
- Formatter: `black`
- Linter: `flake8` or `pylint`
- Type checker: `mypy`

### JavaScript/Node.js (Narrative Director)

- Follow **ESLint** configuration
- Use **ES6+** features
- Use **async/await** for asynchronous operations
- Maximum line length: **100 characters**
- Use **JSDoc** for documentation

Example:
```javascript
/**
 * Generate adaptive narrative content based on emotion
 * @param {Object} emotionData - Emotion prediction data
 * @param {string} emotionData.dominantEmotion - Primary detected emotion
 * @param {number} emotionData.confidence - Confidence score (0-1)
 * @returns {Promise<Object>} Generated narrative content
 */
async function generateNarrative(emotionData) {
  // Implementation
}
```

**Tools**:
- Formatter: `prettier`
- Linter: `eslint`

### Go (LLM Gateway)

- Follow **Go conventions** and idioms
- Use **gofmt** for formatting
- Use **golint** for linting
- Write **godoc** comments for exported functions

Example:
```go
// CompleteRequest handles LLM completion requests with retry logic
// and error handling. It returns the completion response or an error.
func CompleteRequest(ctx context.Context, req *CompletionRequest) (*CompletionResponse, error) {
    // Implementation
}
```

**Tools**:
- Formatter: `gofmt` or `goimports`
- Linter: `golangci-lint`

### Protocol Buffers

- Use **snake_case** for field names
- Add comments for all messages and fields
- Version your proto files appropriately

Example:
```protobuf
// PlayerBehaviorData represents behavioral metrics collected during gameplay
message PlayerBehaviorData {
  // Unique session identifier for the player
  string session_id = 1;
  
  // Timestamp in milliseconds since epoch
  int64 timestamp_ms = 2;
  
  // Average decision latency in milliseconds
  float decision_latency_ms = 3;
}
```

## Testing Guidelines

### Unit Tests

All new features must include unit tests:

**Python**:
```bash
cd services/emotion-inference
pytest tests/ -v --cov=src
```

**Node.js**:
```bash
cd services/narrative-director
npm test
```

**Go**:
```bash
cd services/llm-gateway
go test ./... -v -cover
```

### Integration Tests

For features that span multiple services, add integration tests:

```bash
docker-compose up -d
# Run integration test suite
docker-compose down
```

### Test Coverage

- Aim for **80%+ code coverage**
- All public APIs must have tests
- Include edge cases and error scenarios

## Pull Request Process

### Before Submitting

1. **Run all tests**:
   ```bash
   make test-emotion
   cd services/narrative-director && npm test
   cd services/llm-gateway && go test ./...
   ```

2. **Check code formatting**:
   ```bash
   # Python
   black services/emotion-inference/src
   
   # JavaScript
   cd services/narrative-director && npm run format
   
   # Go
   cd services/llm-gateway && gofmt -w .
   ```

3. **Update documentation**:
   - Update README.md if adding new features
   - Update API documentation
   - Add inline code comments

4. **Verify Docker builds**:
   ```bash
   docker-compose build
   ```

### Submitting the PR

1. Push your branch to your fork
2. Open a Pull Request against `main` branch
3. Fill out the PR template completely
4. Link any related issues

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

1. At least one maintainer must approve
2. All CI checks must pass
3. No unresolved conversations
4. Branch must be up-to-date with main

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Start service with '...'
2. Send request '...'
3. See error

**Expected behavior**
What should happen

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Docker version: [e.g., 20.10.21]
- Service version: [e.g., 0.1.0]

**Logs**
Relevant log output
```

### Feature Requests

Use the feature request template:

```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
Clear description of desired functionality

**Describe alternatives you've considered**
Alternative solutions or features

**Additional context**
Any other context, mockups, or examples
```

## Questions?

- Open a [GitHub Discussion](https://github.com/yourusername/empath-engine/discussions)
- Join our community chat
- Email: dev@synapticneurogaming.com

Thank you for contributing to Empath Engine! 🎉
