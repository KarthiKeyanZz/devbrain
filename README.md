# 🧠 DevBrain - AI-Powered Observability & Debugging Platform

> Intelligent log ingestion, real-time anomaly detection, and deep learning-based root cause analysis for distributed systems

---

Version : 1.0.0

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Project Structure](#project-structure)

---

## 🎯 Overview

DevBrain is an AI-powered observability platform designed to help developers:

- **Ingest** logs, metrics, and events from microservices
- **Detect** anomalies in real-time
- **Analyze** root causes using machine learning
- **Diagnose** system behavior through deep learning

### Key Features

✅ **Real-time Log Ingestion** - FastAPI endpoints for log collection  
✅ **Semantic Search** - Find logs using natural language, not just keywords  
✅ **Anomaly Detection** - Automatically detect suspicious patterns  
✅ **AI-Powered Analysis** - Get insights via Deep Learning models  
✅ **Clustering** - Group similar logs together  
✅ **Docker-ready** - Run everything locally with docker-compose  
✅ **Zero Cost** - Uses open-source tools and local models

---

## 🏗️ Architecture

### High-Level Data Flow

```
[Services] 
    ↓
[FastAPI Ingestion API]
    ↓
[Kafka Message Queue]
    ↓
[Processing Workers] ← ML Pipeline (Embeddings, Clustering, Anomaly Detection)
    ↓
[Storage Layer] (PostgreSQL + Elasticsearch + Redis)
    ↓
[Query API] ← AI Engine (Deep Learning for root cause analysis)
    ↓
[React Dashboard + Chat Interface]
```

### Core Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Ingestion API** | Accept logs from services | FastAPI + Python |
| **Kafka** | Distribute logs for processing | Kafka (Confluent) |
| **PostgreSQL** | Store metadata | PostgreSQL 15 |
| **Elasticsearch** | Full-text log search | Elasticsearch 8.8 |
| **Redis** | Caching layer | Redis 7 |
| **ML Pipeline** | Embeddings, clustering, anomaly detection | Transformers, scikit-learn |
| **DL Models** | Root cause analysis | PyTorch / TensorFlow |
| **Frontend** | Dashboard and chat UI | React + Tailwind CSS |

### Database Schema

```sql
-- Services
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    created_at TIMESTAMP
);

-- Log Metadata
CREATE TABLE logs_metadata (
    id SERIAL PRIMARY KEY,
    service_id INT REFERENCES services(id),
    log_level VARCHAR(50),
    timestamp TIMESTAMP,
    latency_ms FLOAT,
    es_doc_id VARCHAR(255),
    cluster_id INT,
    created_at TIMESTAMP
);

-- Anomalies
CREATE TABLE anomalies (
    id SERIAL PRIMARY KEY,
    service_id INT REFERENCES services(id),
    anomaly_score FLOAT,
    feature_type VARCHAR(50),
    detected_at TIMESTAMP,
    status VARCHAR(50),  -- pending, analyzed, resolved
    root_cause TEXT,
    suggested_action TEXT,
    created_at TIMESTAMP
);

-- Events
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    service_id INT REFERENCES services(id),
    event_type VARCHAR(100),  -- deployment, error_spike, restart
    timestamp TIMESTAMP,
    details TEXT,
    created_at TIMESTAMP
);
```

---

## 💾 Tech Stack

### Backend
- **Framework**: FastAPI (async, high-performance)
- **Database**: PostgreSQL (relational), Elasticsearch (search)
- **Cache**: Redis
- **Streaming**: Kafka
- **ML**: Sentence Transformers, scikit-learn, PyTorch

### Frontend 
- React 18
- Tailwind CSS
- Socket.io for real-time updates

### DevOps
- Docker & Docker Compose
- Python 3.11+

### Deep Learning
- PyTorch/TensorFlow models
- For root cause classification

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Git

### 1. Clone and Setup

```bash
git clone <repo>
cd devbrain

# Create .env file (optional, uses defaults)
cat > .env << EOF
DATABASE_URL=postgresql://devbrain:devbrain@localhost:5432/devbrain
ELASTICSEARCH_HOST=localhost
REDIS_HOST=localhost
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
EOF
```

### 2. Start All Services

```bash
docker-compose up -d
```

This starts:
- ✅ PostgreSQL (port 5432)
- ✅ Elasticsearch (port 9200)
- ✅ Redis (port 6379)
- ✅ Kafka (port 9092)
- ✅ FastAPI Backend (port 8000)

### 3. Initialize Database

```bash
# Inside the backend container or locally
python scripts/seed_data.py
```

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/api/health

# Create a log
curl -X POST http://localhost:8000/api/logs \
  -H "Content-Type: application/json" \
  -d '{
    "service": "payment-service",
    "message": "Payment processed successfully",
    "log_level": "INFO",
    "latency_ms": 150.5
  }'

# Interactive API docs
open http://localhost:8000/docs
```

### 5. Generate Sample Data

```bash
# Continuous log generation
python scripts/log_generator.py --mode continuous --interval 1.0

# Or batch generation
python scripts/log_generator.py --mode batch --count 100
```

### 6. Download DL Models

```bash
# Instructions for downloading DL models will be provided in Phase 4.
# (Currently in development)
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### Logs

**POST /logs** - Create a single log
```json
{
  "service": "payment-service",
  "message": "Payment processed",
  "log_level": "INFO",
  "timestamp": "2024-03-23T10:30:00Z",
  "latency_ms": 150.5,
  "metadata": {"user_id": "123"}
}
```

**POST /logs/batch** - Batch ingest logs
```json
{
  "logs": [
    {"service": "...", "message": "...", ...},
    {"service": "...", "message": "...", ...}
  ]
}
```

**POST /logs/search** - Semantic search
```json
{
  "query": "database connection failed",
  "service": "payment-service",
  "log_level": "ERROR",
  "size": 10
}
```

**GET /logs** - List logs with pagination
```
/logs?service=payment-service&log_level=ERROR&skip=0&limit=100
```

**GET /logs/service/{service_name}/stats** - Service statistics
```
/logs/service/payment-service/stats
```

#### Anomalies

**GET /anomalies** - List detected anomalies
```
/anomalies?service_id=1&status=pending&limit=50
```

**POST /anomalies/{id}/analyze** - Analyze anomaly with AI
```json
{
  "lookback_minutes": 60
}
```

**POST /anomalies/{id}/acknowledge** - Mark as acknowledged
```json
{
  "notes": "Already investigating"
}
```

#### AI/Chat

**POST /ai/chat** - Chat with AI assistant
```json
{
  "message": "Why did my payment service fail?",
  "service_id": 1
}
```

**POST /ai/explain** - Get service explanation
```json
{
  "service_id": 1,
  "from_timestamp": "2024-03-23T09:00:00Z",
  "to_timestamp": "2024-03-23T10:00:00Z",
  "focus": "errors"
}
```

#### Health

**GET /health** - Health check all services
```
response: {
  "status": "healthy",
  "services": {
    "api": "healthy",
    "database": "healthy",
    "redis": "healthy",
    "elasticsearch": "healthy",
    "kafka": "healthy"
  }
}
```

---

## 📚 API Interactive Docs

Swagger UI: `http://localhost:8000/docs`  
ReDoc: `http://localhost:8000/redoc`

---

## 🔄 Development

### Project Structure

```
devbrain/
├── backend/
│   ├── app/
│   │   ├── api/                 # FastAPI route handlers
│   │   │   ├── health.py       # Health check endpoints
│   │   │   ├── logs.py         # Log ingestion & search
│   │   │   ├── anomalies.py    # Anomaly endpoints
│   │   │   └── ai.py           # AI/Chat endpoints
│   │   ├── core/                # Core functionality
│   │   │   ├── config.py       # Settings & configuration
│   │   │   ├── database.py     # PostgreSQL connection
│   │   │   ├── elasticsearch.py # ES integration
│   │   │   ├── kafka.py        # Kafka producer/consumer
│   │   │   └── redis.py        # Redis cache
│   │   ├── models/              # SQLAlchemy ORM models
│   │   │   ├── service.py
│   │   │   ├── log_metadata.py
│   │   │   ├── anomaly.py
│   │   │   └── event.py
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── services/            # Business logic
│   │   │   ├── log_service.py
│   │   │   ├── anomaly_service.py
│   │   │   └── ai_service.py
│   │   ├── ml/                  # Machine learning modules
│   │   │   ├── embedding.py     # Log embeddings
│   │   │   ├── anomaly_detection.py  # Isolation Forest
│   │   │   ├── clustering.py    # DBSCAN
│   │   │   └── vector_store.py  # Vector storage
│   │   ├── workers/             # Async workers
│   │   │   ├── log_worker.py    # Process logs from Kafka
│   │   │   └── anomaly_worker.py # Detect anomalies
│   │   └── utils/
│   │       ├── logger.py        # Logging setup
│   │       └── helpers.py       # Utility functions
│   ├── main.py                  # Application entry point
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile
├── frontend/                    # React dashboard (coming soon)
├── scripts/
│   ├── log_generator.py        # Generate test logs
│   └── seed_data.py            # Initialize database
├── docker-compose.yml          # Multi-container orchestration
└── README.md
```

### Local Development Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start services (in separate terminal)
docker-compose up -d

# Run FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests

```bash
pytest app/tests/ -v
```

### Code Style

```bash
# Format code
black app/

# Lint
pylint app/
```

---

## 📊 Example Workflows

### 1. Ingest Logs from Python Service

```python
import requests

logs = [
    {
        "service": "payment-service",
        "message": "Payment initiated for user 123",
        "log_level": "INFO",
        "latency_ms": 50,
    },
    {
        "service": "payment-service",
        "message": "Database timeout after 30 seconds",
        "log_level": "ERROR",
        "latency_ms": 30000,
    }
]

response = requests.post("http://localhost:8000/api/logs/batch", json={"logs": logs})
print(response.json())
```

### 2. Search Logs Semantically

```bash
curl -X POST http://localhost:8000/api/logs/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "database connection failed",
    "service": "payment-service",
    "size": 10
  }'
```

### 3. Get AI Explanation

```bash
curl -X POST http://localhost:8000/api/ai/explain \
  -H "Content-Type: application/json" \
  -d '{
    "service_id": 1,
    "from_timestamp": "2024-03-23T09:00:00Z",
    "to_timestamp": "2024-03-23T10:00:00Z"
  }'
```

### 4. Chat with AI

```bash
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Why is my service slow?",
    "service_id": 1
  }'
```

---

## 🔍 Monitoring & Debugging

### View Logs

```bash
# Backend logs
docker logs devbrain-backend -f

# All services
docker-compose logs -f
```

### Database Queries

```bash
# Connect to PostgreSQL
psql -U devbrain -d devbrain -h localhost

# List tables
\dt

# Query logs
SELECT * FROM logs_metadata LIMIT 10;
```

### Elasticsearch

```bash
# Check indices
curl http://localhost:9200/_cat/indices

# Search logs
curl http://localhost:9200/logs_index/_search
```

### Kafka Topics

```bash
# List topics
docker exec devbrain-kafka kafka-topics.sh --bootstrap-server localhost:9092 --list

# Monitor topic
docker exec devbrain-kafka kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic logs \
  --from-beginning
```

---

## 🧠 ML/AI Models

### Embedding Model
- **Model**: `all-MiniLM-L6-v2` (from Hugging Face)
- **Size**: ~86MB
- **Dimensions**: 384
- **Use**: Convert log messages to vectors for semantic search

### Anomaly Detection
- **Algorithm**: Isolation Forest (scikit-learn)
- **Features**: Error rate, latency, log frequency
- **Output**: Anomaly scores [0, 1]

### Clustering
- **Algorithm**: DBSCAN (scikit-learn)
- **Input**: Log embeddings
- **Output**: Cluster assignments

### Deep Learning Models
- **Framework**: PyTorch / TensorFlow (planned)
- **Purpose**: Advanced root cause analysis and classification

---

## 📝 Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# Elasticsearch
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_PROTOCOL=http

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_LOG_TOPIC=logs
KAFKA_ANOMALY_TOPIC=anomalies

    # ML Configuration
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIM=384
ANOMALY_THRESHOLD=0.7

# Application
DEBUG=true
LOG_LEVEL=INFO
```

---

## 🐛 Troubleshooting

### Services failing to connect

```
SOLUTION: Run `docker-compose down && docker-compose up -d`
to rebuild containers with updated network configuration
```

### Elasticsearch not responding

```
SOLUTION: Check disk space - Elasticsearch needs ~2GB
docker exec devbrain-elasticsearch curl http://localhost:9200/_cluster/health
```

### Out of memory

```
SOLUTION: Reduce container limits in docker-compose.yml
or increase Docker's memory allocation
```

### Kafka connection refused

```
SOLUTION: Wait 30 seconds after starting - Kafka takes time to initialize
docker logs devbrain-kafka
```

---

## 🚀 Deployment

### To Render (Free Tier)

```bash
# 1. Create Render account
# 2. Connect GitHub repo
# 3. Create Web Service -> Select devbrain repo
# 4. Environment: Python
# 5. Build command: pip install -r backend/requirements.txt
# 6. Start command: cd backend && uvicorn main:app --host 0.0.0.0
# 7. Add environment variables from .env
```

### To Railway (Free Tier)

```bash
# 1. Install Railway CLI
# 2. railway login
# 3. railway init
# 4. Add services via dashboard (PostgreSQL, Redis)
# 5. railway up
```

---

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Elasticsearch Docs](https://www.elastic.co/guide/en/elasticsearch/reference/)
- [Sentence Transformers](https://www.sbert.net/)

---

## 🤝 Contributing

Contributions welcome! Areas needing work:

- [ ] DL integration (deep learning for root cause analysis)
- [ ] React frontend dashboard
- [ ] Real-time WebSocket updates
- [ ] Advanced ML models (LSTM, Transformers)
- [ ] Distributed tracing (OpenTelemetry)
- [ ] Alert rules engine
- [ ] Grafana integration

---

## 📄 License

This project is open source and available under the MIT License.

---

## 📞 Support

- 📧 Email: support@devbrain.ai
- 🐦 Twitter: @devbrainai
- 💬 Discord: [Join Community]

---

**Made with ❤️ for developers who love observability**
