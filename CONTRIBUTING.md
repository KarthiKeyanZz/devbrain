# Contributing to DevBrain

Thank you for your interest in contributing to DevBrain! This document provides guidelines for contributing.

## Development Setup

### Local Environment

```bash
# Clone the repository
git clone <repo>
cd devbrain

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r backend/requirements.txt
pip install black pylint pytest pytest-asyncio

# Start all services
docker-compose up -d

# Run migrations (if needed)
# python -m alembic upgrade head
```

### Code Style

We follow PEP 8 with a few modifications:

- **Line length**: 100 characters
- **Formatter**: Black
- **Linter**: Pylint

```bash
# Format code
black backend/

# Lint code
pylint backend/app/

# Run tests
pytest backend/app/tests/
```

## Areas for Contribution

### Phase 2: ML/AI Features (In Progress)

- [ ] **Embedding Pipeline** - Implement real Sentence Transformers
- [ ] **Anomaly Detection** - Complete Isolation Forest integration
  - [ ] **Log Clustering** - Implement DBSCAN
- [ ] **DL Integration** - Connect Deep Learning models for root cause analysis

### Phase 3: API Enhancements

- [ ] Implement AI Explanation endpoints
- [ ] Add advanced filtering in search
- [ ] Implement batch processing workers
- [ ] Add authentication/authorization

### Phase 4: Frontend Dashboard

- [ ] React component library
- [ ] Real-time log streaming (WebSocket)
- [ ] Anomaly dashboard
- [ ] Chat interface

### Phase 5: DevOps & Deployment

- [ ] Kubernetes manifests
- [ ] GitHub Actions CI/CD
- [ ] Monitoring setup (Prometheus, Grafana)
- [ ] Documentation site (Sphinx)

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run tests and linting locally
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Commit Message Guidelines

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only
- `style`: Changes that don't affect code meaning
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build/dependency changes

Example:
```
feat(logs): implement semantic search with embeddings

Implement semantic search using Sentence Transformers
to find similar logs. Uses cosine similarity on embeddings
stored in Elasticsearch.

Closes #123
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest app/tests/test_logs.py

# Run with coverage
pytest --cov=app

# Run specific test
pytest app/tests/test_logs.py::test_create_log
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all functions
- Update API docs in comments

## Project Structure

```
devbrain/
├── backend/          # Python backend
├── frontend/         # React frontend
├── scripts/          # Utility scripts
└── docs/            # Documentation
```

## Questions?

- Open an issue for bugs
- Start a discussion for features
- Check existing issues first

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

---

Happy contributing! 🎉
