# ⚙️ Enterprise Car Rental — Backend Tier

This repository houses the two backend microservices powering the Car Rental platform:

1. **`backend-gateway/`**: **NestJS 10 API Gateway** with Swagger OpenAPI docs, DTO validation, Vehicle & Booking lifecycle management, Analytics aggregation, and Event-driven Webhooks.
2. **`ai-service/`**: **Python 3.12 + FastAPI AI & RAG Microservice** with in-memory Cosine Similarity Vector Store, Gemini 2.0/1.5 Flash grounded prompt generator, and automated AI Lead Qualifier.

---

## 🏗️ Architecture & Modules

```
backend/
├── ai-service/                   # Python 3.12 FastAPI RAG Microservice
│   ├── app/
│   │   ├── api/                  # RAG and Lead Scoring routes
│   │   ├── core/                 # Config & Knowledge Base Chunks
│   │   └── services/             # Vector Store, RAG Engine, Lead Scorer
│   ├── tests/                    # Pytest test suite (RAG, Vector, Scorer)
│   ├── Dockerfile
│   └── requirements.txt
│
└── backend-gateway/              # NestJS 10 Core API Gateway
    ├── src/
    │   ├── modules/
    │   │   ├── vehicles/         # Vehicle fleet CRUD & filters
    │   │   ├── bookings/         # Booking state machine & calculations
    │   │   ├── analytics/        # KPI and trends aggregation
    │   │   ├── ai-proxy/         # Secure HTTP proxy to AI Microservice
    │   │   └── automation/       # Webhook & event-driven lead triggers
    │   ├── main.ts
    │   └── app.module.ts
    ├── test/
    ├── Dockerfile
    └── package.json
```

---

## 🧪 Testing

```bash
# Test AI Microservice
cd ai-service
pytest -v

# Test Backend Gateway
cd backend-gateway
npm test
npm run build
```

---

## 🚀 Branch Promotion Workflow

```
feat/* -> test -> dev -> main
```
All pull requests and merges must pass CI validations in `.github/workflows/ci.yml`.
