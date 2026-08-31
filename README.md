# 🚗 Best Care — Enterprise Backend & Intelligent AI Ecosystem

An enterprise-grade, high-concurrency distributed backend ecosystem powering the **Best Care Smart Car Rental Platform**. The backend combines a robust **NestJS 10 API Gateway** with an advanced **FastAPI Multilingual Agentic RAG (Retrieval-Augmented Generation) AI Microservice**. It delivers full-scale fleet automation, conversational AI car booking, multi-turn slot filling, dynamic surge pricing, real-time availability scheduling, event-driven webhooks, and executive business analytics.

---

## 📑 Table of Contents
1. [System Architecture Overview](#-system-architecture-overview)
2. [Complete Feature Matrix](#-complete-feature-matrix)
3. [Deep Dive: How the Agentic RAG Pipeline Works](#-deep-dive-how-the-agentic-rag-pipeline-works)
   - [RAG Architecture & Execution Workflow Diagram](#rag-architecture--execution-workflow-diagram)
   - [Multilingual Query Planner & Intent Router](#1-multilingual-query-planner--intent-router)
   - [Dual-Path Hybrid Search (Vector + BM25)](#2-dual-path-hybrid-search-vector--bm25)
   - [Reciprocal Rank Fusion (RRF) & Cross-Encoder Reranking](#3-reciprocal-rank-fusion-rrf--cross-encoder-reranking)
   - [Conversational Slot-Filling Booking Agent](#4-conversational-slot-filling-booking-agent)
   - [Dynamic Context Builder & Token Budgeting](#5-dynamic-context-builder--token-budgeting)
   - [Grounded LLM Generation & Factuality Guardrails](#6-grounded-llm-generation--factuality-guardrails)
   - [Asynchronous Knowledge Ingestion & Sync Pipeline](#7-asynchronous-knowledge-ingestion--sync-pipeline)
4. [Deep Dive: Backend Gateway Modules (NestJS)](#-deep-dive-backend-gateway-modules-nestjs)
   - [1. Auth & RBAC Module (`/auth`)](#1-auth--rbac-module-auth)
   - [2. Vehicles & Fleet Operations Module (`/vehicles`)](#2-vehicles--fleet-operations-module-vehicles)
   - [3. Cars Public Showcase Module (`/cars`)](#3-cars-public-showcase-module-cars)
   - [4. Bookings State Machine Engine (`/bookings`)](#4-bookings-state-machine-engine-bookings)
   - [5. Availability & Conflict Prevention Module (`/availability`)](#5-availability--conflict-prevention-module-availability)
   - [6. Dynamic Pricing & Surge Engine (`/pricing`)](#6-dynamic-pricing--surge-engine-pricing)
   - [7. Payments, Billing & Invoicing Module (`/payments`)](#7-payments-billing--invoicing-module-payments)
   - [8. Business Intelligence & Analytics Module (`/analytics`)](#8-business-intelligence--analytics-module-analytics)
   - [9. Executive Reports Module (`/reports`)](#9-executive-reports-module-reports)
   - [10. Verified Customer Reviews Module (`/reviews`)](#10-verified-customer-reviews-module-reviews)
   - [11. AI Proxy Bridge Module (`/ai`)](#11-ai-proxy-bridge-module-ai)
   - [12. Webhooks & Automation Module (`/automation`)](#12-webhooks--automation-module-automation)
5. [Deep Dive: AI Microservice Modules (FastAPI)](#-deep-dive-ai-microservice-modules-fastapi)
6. [Complete REST API Reference](#-complete-rest-api-reference)
   - [Gateway Endpoints (`http://localhost:3001`)](#1-gateway-endpoints-httplocalhost3001)
   - [AI Microservice Endpoints (`http://localhost:8000`)](#2-ai-microservice-endpoints-httplocalhost8000)
7. [Security, Performance & Enterprise Guardrails](#-security-performance--enterprise-guardrails)
8. [Repository & Directory Structure](#-repository--directory-structure)
9. [Step-by-Step Installation & Local Setup](#-step-by-step-installation--local-setup)
10. [Docker & Containerized Deployment](#-docker--containerized-deployment)
11. [Testing & Quality Assurance](#-testing--quality-assurance)

---

## 🏛️ System Architecture Overview

The backend is built as a microservices architecture engineered for high concurrency, low latency, fault tolerance, and clean domain separation.

```
                               ┌────────────────────────────┐
                               │   Frontend Client Layer    │
                               │   (Next.js 15 App Router)  │
                               └─────────────┬──────────────┘
                                             │
                                             │ REST / JSON / JWT / WebSockets
                                             ▼
                 ┌──────────────────────────────────────────────────────────┐
                 │                   NestJS API Gateway                     │
                 │              (Port: 3001 | Traffic Hub)                  │
                 │                                                          │
                 │ • JWT Auth, Password Hashing & Role Guards               │
                 │ • Request DTO Validation (class-validator)               │
                 │ • Global Exception Filter & Structured Logging           │
                 │ • Rate Limiting & Helmet Security Middleware             │
                 └───────────┬──────────────────────────────┬───────────────┘
                             │                              │
              ┌──────────────┘                              └──────────────┐
              ▼                                                            ▼
┌───────────────────────────────────────────┐    HTTP / IPC  ┌───────────────────────────────────────────┐
│           Core Business Hub               │◄──────────────►│         FastAPI AI Microservice           │
│                                           │ (Internal Sync)│        (Port: 8000 | Agentic Core)        │
│ • Vehicles Fleet Lifecycle Management     │                │                                           │
│ • Finite State Machine Booking Engine     │                │ • Multilingual Query Parser (BN/EN/Mixed) │
│ • Availability Calendar & Conflict Checks │                │ • Intent Classifier & Entity Extractor    │
│ • Dynamic Surge Pricing & Discounts       │                │ • Dual-Path Hybrid Search (Vector + BM25) │
│ • Payments, Invoicing & Receipts          │                │ • Reciprocal Rank Fusion (RRF) & Rerank   │
│ • Executive Analytics & KPI Aggregators   │                │ • Conversational Slot-Filling Agent       │
│ • Customer Reviews & Star Ratings         │                │ • Grounded Gemini 2.0/1.5 Flash Generator │
│ • Automated CRM Webhooks & Lead Scorer    │                │ • Factuality & Hallucination Guardrails   │
└───────────────────────────────────────────┘                └───────────────────────────────────────────┘
```

---

## ⚡ Complete Feature Matrix

| Feature Area | Feature Detail & Capability | Implemented In |
| :--- | :--- | :--- |
| **Authentication & RBAC** | JWT issue/verify, refresh tokens, role guards (`ADMIN`, `CUSTOMER`, `DRIVER`, `STAFF`), bcrypt hashing. | Gateway (`/auth`) |
| **Fleet Management** | Full CRUD, vehicle status switcher (`AVAILABLE`, `RENTED`, `MAINTENANCE`, `UNAVAILABLE`), category tags. | Gateway (`/vehicles`, `/cars`) |
| **Vehicle Specifications** | Fuel (Octane, Hybrid, Electric, Diesel), Transmission (Auto, Manual), Seating (4, 5, 7, 10+), GPS, Dashcam. | Gateway (`/vehicles`) |
| **Booking Engine** | State machine (`PENDING`, `CONFIRMED`, `ACTIVE`, `COMPLETED`, `CANCELLED`), auto reference code (`BK-XXXXX`). | Gateway (`/bookings`) |
| **Price Calculations** | Hourly & daily base rates, rental duration calculator, tax/VAT estimation, add-on package calculations. | Gateway (`/bookings/calculate-price`) |
| **Add-On Packages** | Full insurance protection, child safety seat, extra chauffeur, airport doorstep delivery. | Gateway (`/bookings`) |
| **Conflict-Free Scheduling**| Date-range collision detection algorithm preventing overlapping bookings for the same vehicle. | Gateway (`/availability`) |
| **Dynamic Surge Pricing** | Weekend multipliers, holiday peak rates, long-term duration discounts (weekly/monthly). | Gateway (`/pricing`) |
| **Payments & Invoicing** | Digital payment intents, card/cash validation, transaction history, itemized invoice breakdown. | Gateway (`/payments`) |
| **Executive Analytics** | Total revenue, active rentals, fleet utilization %, average rental days, monthly revenue vs expenses. | Gateway (`/analytics`) |
| **Verified Reviews** | Multi-criteria ratings (Cleanliness, Driver, Punctuality, Comfort), verified booking check, score averaging. | Gateway (`/reviews`) |
| **Webhooks & Automation** | Event-driven triggers, high-intent lead alerts, automated customer SMS/email simulations. | Gateway (`/automation`) |
| **AI Multilingual Support**| Full natural language understanding for English, Bengali (বাংলা), and transliterated Banglish. | AI Service (`/rag/chat`) |
| **Hybrid Search (RAG)** | Dense vector embeddings (`text-embedding-004`) + Sparse BM25 keyword matching + RRF fusion. | AI Service (`/rag/search`) |
| **Slot-Filling Booking Agent**| Multi-turn conversation collecting pickup date, return date, location, car type with confirmation. | AI Service (`app/booking`) |
| **Grounded Generation** | Strict system prompts ensuring LLM answers strictly from verified knowledge chunks with zero hallucinations. | AI Service (`app/generation`)|
| **AI Lead Qualification** | Scores leads (`HOT`, `WARM`, `COLD`) based on conversation urgency, budget clarity, and trip intent. | AI Service (`app/api`) |
| **Asynchronous Indexing** | Ingests vehicle fleet, company policies, FAQs, and updates vector embeddings in the background. | AI Service (`/rag/sync-knowledge`)|

---

## 🧠 Deep Dive: How the Agentic RAG Pipeline Works

The **Retrieval-Augmented Generation (RAG)** pipeline is an asynchronous, multilingual, hybrid search system that transforms conversational user inputs into verified answers and automated booking workflows.

### RAG Architecture & Execution Workflow Diagram

```
                     ┌──────────────────────────────────────────────────────────┐
                     │             User Query (BN / EN / Banglish)              │
                     │   e.g., "Ami family niye 3 din Cox's Bazar jabo,        │
                     │          7 seater SUV er khoroch koto hobe?"             │
                     └────────────────────────────┬─────────────────────────────┘
                                                  │
                                                  ▼
                     ┌──────────────────────────────────────────────────────────┐
                     │             1. Multilingual Query Planner                │
                     │  • Language Detection (Bengali / English / Banglish)     │
                     │  • Intent Classification (Booking / Policy / Pricing)    │
                     │  • Entity Extraction (Dates, Locations, Passengers, Car) │
                     │  • Query Rewriting & Expansion (Synonym resolution)      │
                     └────────────────────────────┬─────────────────────────────┘
                                                  │
                 ┌────────────────────────────────┴────────────────────────────────┐
                 ▼                                                                 ▼
┌─────────────────────────────────────────────────┐               ┌─────────────────────────────────────────────────┐
│            A. Booking Action Route              │               │            B. Hybrid Retrieval Route            │
│                                                 │               │                                                 │
│ • State Machine Slot Validator                  │               │   ┌─────────────────────────────────────────┐   │
│   (Checks: pickup_date, return_date, car_type)  │               │   │ 2a. Dense Semantic Vector Search        │   │
│ • Slot-Filling Follow-up Question Generator     │               │   │     (Cosine Similarity on Embeddings)   │   │
│ • Vehicle Catalog Query Matcher                 │               │   └────────────────────┬────────────────────┘   │
│ • Pre-Booking Action Payload Assembly           │               │                        │                        │
└────────────────────────┬────────────────────────┘               │   ┌────────────────────┴────────────────────┐   │
                         │                                        │   │ 2b. Sparse Lexical Keyword Search       │   │
                         │                                        │   │     (BM25 Exact & Fuzzy Matching)       │   │
                         │                                        │   └────────────────────┬────────────────────┘   │
                         │                                        │                        │                        │
                         │                                        │   ┌────────────────────▼────────────────────┐   │
                         │                                        │   │ 3. Reciprocal Rank Fusion (RRF)         │   │
                         │                                        │   │    RRF Score = Σ 1 / (60 + rank_i)      │   │
                         │                                        │   └────────────────────┬────────────────────┘   │
                         │                                        │                        │                        │
                         │                                        │   ┌────────────────────▼────────────────────┐   │
                         │                                        │   │ 4. Cross-Encoder Reranker               │   │
                         │                                        │   │    Re-scores top K candidate passages   │   │
                         │                                        │   └────────────────────┬────────────────────┘   │
                         │                                        └────────────────────────┼────────────────────────┘
                         │                                                                 │
                         └────────────────────────────────┬────────────────────────────────┘
                                                          │
                                                          ▼
                     ┌──────────────────────────────────────────────────────────┐
                     │                5. Dynamic Context Builder                │
                     │  • Injects Multi-turn Conversation Sliding Window Memory │
                     │  • Injects User Profile & Active Session State           │
                     │  • Passage Deduplication & Token Budget Control          │
                     └────────────────────────────┬─────────────────────────────┘
                                                  │
                                                  ▼
                     ┌──────────────────────────────────────────────────────────┐
                     │          6. Grounded LLM Generation (Gemini)             │
                     │  • Strict System Prompts (Answer ONLY from context)      │
                     │  • Preserves Query Language (Responds in Bangla if asked)│
                     │  • Generates Interactive UI Cards (Vehicles & CTA)       │
                     └────────────────────────────┬─────────────────────────────┘
                                                  │
                                                  ▼
                     ┌──────────────────────────────────────────────────────────┐
                     │          7. Factuality & Hallucination Guard             │
                     │  • Compares generated answer against retrieved facts     │
                     │  • Checks for pricing discrepancies or unverified claims │
                     │  • Auto-fallback to Customer Support Hotline if ungrounded│
                     └────────────────────────────┬─────────────────────────────┘
                                                  │
                                                  ▼
                     ┌──────────────────────────────────────────────────────────┐
                     │        Final JSON Response (Message, Data, Cards)        │
                     └──────────────────────────────────────────────────────────┘
```

---

### 1. Multilingual Query Planner & Intent Router
- **Language Detection**: Uses regex character block detection (Unicode `\u0980-\u09FF` for Bengali script) and phonetic n-gram heuristics to identify English, Bengali, and Banglish transliteration.
- **Intent Classification**: Classifies queries into 6 distinct operational intents:
  1. `booking_action`: User wants to reserve a car or requests availability for a trip.
  2. `policy_inquiry`: User asks about security deposits, fuel policies, driver requirements, or cancellation terms.
  3. `pricing_query`: User asks for daily rates, discount packages, or extra add-on costs.
  4. `vehicle_spec`: User asks for specific car features (e.g., "Prado mileage", "HiAce seating capacity").
  5. `lead_qualification`: High-intent corporate or multi-day trip inquiry requiring priority follow-up.
  6. `general_chitchat`: Greetings and general conversational queries.
- **Entity Extraction**: Automatically extracts `location`, `pickup_date`, `return_date`, `passenger_count`, `budget`, and `vehicle_category`.

---

### 2. Dual-Path Hybrid Search (Vector + BM25)
To achieve maximum retrieval recall and precision:
- **Dense Semantic Retrieval**:
  - The query is encoded into high-dimensional vector space using Google `text-embedding-004`.
  - Computes cosine similarity against all pre-indexed knowledge base embeddings:
    $$\text{Cosine Similarity}(u, v) = \frac{u \cdot v}{\|u\| \|v\|}$$
- **Sparse Lexical Search (BM25)**:
  - Tokenizes the query into keywords and calculates BM25 term frequency-inverse document frequency scores.
  - Guarantees exact matches for car model names (e.g., "Noah", "Axio", "Premio", "Prado"), license plate terms, and specific numeric pricing.

---

### 3. Reciprocal Rank Fusion (RRF) & Cross-Encoder Reranking
- **Reciprocal Rank Fusion (RRF)**:
  Merges the ranked lists of Dense and Sparse retrievers using the standard RRF algorithm:
  $$RRF(d) = \sum_{m \in \{\text{Dense}, \text{Sparse}\}} \frac{1}{k + r_m(d)}$$
  *(where $k = 60$, and $r_m(d)$ is the 1-based rank position of document $d$ in retrieval method $m$)*.
- **Cross-Encoder Reranker**:
  The top 10 fused candidates are passed through a cross-encoder model that scores query-document interaction with full attention to eliminate semantic false positives.

---

### 4. Conversational Slot-Filling Booking Agent
When `intent == booking_action`:
1. The agent inspects the session state for required booking slots:
   - `[x] pickup_location`
   - `[x] destination / return_location`
   - `[ ] pickup_date`
   - `[ ] return_date`
   - `[ ] vehicle_type / seating_capacity`
2. If any slot is missing, the agent generates a friendly, conversational follow-up in the user's language (e.g., *"Apni kon tarikh theke kon tarikh porjonto gariti nite chachhen?"*).
3. Once all slots are collected, the agent queries the vehicle catalog for matching available vehicles and returns structured JSON cards with direct *"Book Now"* triggers.

---

### 5. Dynamic Context Builder & Token Budgeting
- **Sliding Window Memory**: Maintains the last $N$ turns of conversational dialogue to preserve multi-turn context (e.g., remembering that the user asked for a 7-seater two messages ago).
- **Token Budgeting**: Allocates strict token ceilings (e.g., 2,048 tokens for context chunks, 512 tokens for memory, 512 tokens for instructions).
- **Deduplication**: Filters out redundant passages from adjacent chunks covering the same vehicle or policy.

---

### 6. Grounded LLM Generation & Factuality Guardrails
- **Prompt Engineering**: Uses structured prompt templates injecting retrieved knowledge passages into `<context></context>` XML blocks.
- **Strict Grounding Directive**: Gemini is explicitly instructed:
  > *"You are the Best Care AI Concierge. Answer strictly based on the provided context. Never invent prices, car models, or policies not present in the context. If context is insufficient, politely inform the user and provide the support hotline."*
- **Factuality Guard**: Inspects the generated output for hallucinated numbers or vehicle models not present in the retrieved passages before returning to the user.

---

### 7. Asynchronous Knowledge Ingestion & Sync Pipeline
- Ingests structured and unstructured knowledge:
  - Real-time fleet inventory (specs, rates, features).
  - Rental terms, insurance tiers, security deposits, and cancellation policies.
  - Driver guidelines, airport transfer rates, and branch locations.
- Chunks text into semantically coherent 300-500 character fragments with 50-character overlap.
- Computes vector embeddings in background worker threads without blocking live customer traffic.

---

## 🚀 Deep Dive: Backend Gateway Modules (NestJS)

The **NestJS API Gateway** (`backend-gateway/`) contains 12 specialized enterprise modules:

### 1. Auth & RBAC Module (`/auth`)
- **Authentication Strategy**: Issues JWT tokens signed with HMAC-SHA256.
- **Password Security**: Hashes user passwords with `bcrypt` (10 salt rounds).
- **Role-Based Access Control**: Decorators (`@Roles('ADMIN', 'CUSTOMER', 'DRIVER')`) and `RolesGuard` enforcing endpoint permissions.
- **Token Rotation**: Endpoint to refresh expired access tokens using valid refresh tokens.

### 2. Vehicles & Fleet Operations Module (`/vehicles`)
- **Lifecycle Management**: Endpoints to create, update, inspect, and decommission vehicles.
- **Status Machine**: Real-time status transitions (`AVAILABLE` ➔ `RENTED` ➔ `MAINTENANCE` ➔ `UNAVAILABLE`).
- **Comprehensive Filtering**: Query params for `category`, `fuelType`, `transmission`, `minPrice`, `maxPrice`, `seats`, and `isFeatured`.
- **Search Engine**: Case-insensitive keyword matching across vehicle brand, model, and year.

### 3. Cars Public Showcase Module (`/cars`)
- **Optimized Read-Only Catalog**: High-performance cached endpoints for public browsing.
- **Featured Fleet**: Delivers highlighted vehicles for homepage carousels and promotional sections.

### 4. Bookings State Machine Engine (`/bookings`)
- **Lifecycle State Machine**:
  ```
  [PENDING] ──(Admin Confirms)──► [CONFIRMED] ──(Trip Starts)──► [ACTIVE] ──(Vehicle Returned)──► [COMPLETED]
     │                                │                                │
     └──────(Customer Cancels)────────┴───────(Admin Cancels)──────────┴──────────────────────► [CANCELLED]
  ```
- **Price Calculation Service**:
  - Daily base rate $\times$ duration (days).
  - Hourly rate for partial-day extensions.
  - Add-on fees (Comprehensive Insurance: +1,500 BDT/day, Child Seat: +500 BDT, Chauffeur: +1,000 BDT/day).
  - Estimated tax/VAT (5%).
- **Booking Reference Generator**: Generates unique alphanumeric codes (e.g., `BK-84920`).
- **Customer Lookup**: `/bookings/my-bookings` automatically filters reservations by authenticated JWT user ID.

### 5. Availability & Conflict Prevention Module (`/availability`)
- **Collision Detection**: Validates requested rental date ranges against active bookings to ensure zero double-bookings:
  $$\text{Collision} = (\text{Start}_{\text{new}} \le \text{End}_{\text{existing}}) \land (\text{End}_{\text{new}} \ge \text{Start}_{\text{existing}})$$
- **Calendar Matrix**: Returns monthly availability calendar for all vehicles in the fleet.

### 6. Dynamic Pricing & Surge Engine (`/pricing`)
- **Surge Modifiers**: Applies dynamic multipliers based on:
  - Weekend rentals (+15% surge).
  - National holidays & festival seasons (+25% surge).
  - Extended rentals (> 7 days: -10% discount, > 30 days: -20% discount).

### 7. Payments, Billing & Invoicing Module (`/payments`)
- **Payment Intent Lifecycle**: Initializes payment transactions with transaction ID tracking.
- **Payment Modes**: Supports Card, Digital Wallets, and Cash on Delivery.
- **Invoice Breakdown**: Generates itemized billing breakdowns (Base cost, add-ons, taxes, total paid, balance due).

### 8. Business Intelligence & Analytics Module (`/analytics`)
- **Executive KPIs**:
  - `totalRevenue`: Cumulative gross revenue.
  - `activeRentals`: Currently deployed vehicles.
  - `fleetUtilizationRate`: $\frac{\text{Active Rentals}}{\text{Total Fleet Size}} \times 100\%$.
  - `totalBookings`: Count of completed and pending bookings.
  - `conversionRate`: Visitor to confirmed booking conversion percentage.
- **Chart Data Providers**:
  - Monthly revenue vs expenses array formatted for Recharts.
  - Fleet category distribution share for Donut charts.

### 9. Executive Reports Module (`/reports`)
- **Financial Summaries**: Aggregates revenue by vehicle category, location, and payment method.
- **Fleet Maintenance Reports**: Tracks service history and downtime costs.

### 10. Verified Customer Reviews Module (`/reviews`)
- **Multi-Criteria Scoring**: 1-5 star ratings for Cleanliness, Driver Professionalism, Punctuality, and Comfort.
- **Verification Guard**: Ensures reviews can only be submitted for completed bookings.
- **Aggregate Rating**: Computes average vehicle score displayed on public fleet cards.

### 11. AI Proxy Bridge Module (`/ai`)
- **Microservice Communication**: Forwarding customer chat messages and search queries to the FastAPI RAG service.
- **Fault Tolerance**: Automatic fallback responses if the AI service undergoes maintenance or rate limits.

### 12. Webhooks & Automation Module (`/automation`)
- **Event-Driven Triggers**: Dispatches webhooks when bookings are created, confirmed, or cancelled.
- **High-Intent Lead Triggers**: Automatically notifies sales personnel when AI classifies a customer query as `HOT` lead.

---

## 🤖 Deep Dive: AI Microservice Modules (FastAPI)

```
backend/ai-service/app/
├── api/
│   └── routes.py                 # REST routes for /rag/chat, /rag/search, /rag/sync-knowledge
├── booking/
│   ├── booking_handler.py        # Conversational slot-filling state machine
│   └── slot_filler.py            # Entity extractor and missing slot validator
├── context/
│   └── context_builder.py        # Token budgeting, passage deduplication, memory injection
├── core/
│   ├── config.py                 # Pydantic v2 settings (API keys, ports, model names)
│   └── logging.py                # Structured JSON logging
├── generation/
│   ├── llm_generator.py          # Gemini 2.0/1.5 Flash grounded prompt generator
│   └── grounding_guard.py        # Factuality validator and anti-hallucination guard
├── indexing/
│   └── dynamic_knowledge_syncer.py# Asynchronous knowledge chunking and vector indexer
├── memory/
│   └── conversation_memory.py    # Multi-turn conversation sliding window buffer
├── query/
│   ├── query_planner.py          # Query analysis, intent classification, and entity routing
│   └── multilingual_parser.py    # Bangla, English, Banglish language detector
└── retrieval/
    ├── hybrid_retriever.py       # Dense vector (Cosine) + Sparse (BM25) + RRF fusion
    └── reranker.py               # Cross-encoder precision passage reranker
```

---

## 📡 Complete REST API Reference

### 1. Gateway Endpoints (`http://localhost:3001`)

#### Authentication (`/auth`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/register` | Register customer/driver account | No |
| `POST` | `/auth/login` | Login with email & password, returns JWT | No |
| `GET` | `/auth/profile` | Get currently logged-in user profile | Bearer JWT |
| `POST` | `/auth/refresh` | Refresh access token | Bearer JWT |

#### Vehicles & Fleet (`/vehicles` & `/cars`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/vehicles` | List all vehicles with category/price/seats filters | No |
| `GET` | `/vehicles/:id` | Get full vehicle specifications and images | No |
| `POST` | `/vehicles` | Add new vehicle to fleet | Admin / Manager |
| `PATCH` | `/vehicles/:id` | Update vehicle details | Admin / Manager |
| `PATCH` | `/vehicles/:id/status` | Update status (Available/Rented/Maintenance) | Admin / Staff |
| `DELETE`| `/vehicles/:id` | Remove vehicle from fleet | Admin |
| `GET` | `/cars/featured` | Get featured vehicle catalog | No |

#### Bookings (`/bookings`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/bookings` | Create new vehicle booking | Customer / Admin |
| `GET` | `/bookings` | List all bookings with status/date filters | Admin |
| `GET` | `/bookings/my-bookings` | List bookings of logged-in customer | Customer |
| `GET` | `/bookings/:id` | Get booking detail by ID or Reference Code | Authenticated |
| `PATCH` | `/bookings/:id/status` | Advance booking state (Confirm/Activate/Complete/Cancel)| Admin / Staff |
| `POST` | `/bookings/calculate-price` | Calculate rental cost based on dates & add-ons | No |

#### Availability & Pricing (`/availability` & `/pricing`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/availability/check` | Check vehicle availability for date range | No |
| `GET` | `/availability/calendar` | Monthly fleet scheduling calendar | Admin / Staff |
| `GET` | `/pricing/rules` | Retrieve active base rates and surge multipliers | No |
| `POST` | `/pricing/rules` | Update pricing rules and discounts | Admin |

#### Payments & Billing (`/payments`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/payments/create-intent`| Initialize payment for a booking | Customer |
| `POST` | `/payments/verify` | Verify digital payment transaction | Authenticated |
| `GET` | `/payments/booking/:id` | Get itemized invoice and receipts | Authenticated |

#### Business Analytics (`/analytics`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/analytics/overview` | KPI overview (Revenue, Fleet Utilization, Bookings) | Admin |
| `GET` | `/analytics/revenue-trends`| Monthly revenue vs expense breakdown for charts | Admin |
| `GET` | `/analytics/fleet-distribution`| Fleet category distribution share for charts | Admin |

#### AI Proxy (`/ai`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/ai/chat` | Proxy customer message to FastAPI RAG Service | No / Customer |

---

### 2. AI Microservice Endpoints (`http://localhost:8000`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/rag/chat` | Main Agentic RAG chat endpoint (intent, slot-filling, hybrid search, grounded LLM) |
| `POST` | `/rag/search` | Direct hybrid semantic + BM25 search for testing retrieval recall |
| `POST` | `/rag/query-plan` | Inspects query parsing, language detection, and entity extraction |
| `POST` | `/rag/sync-knowledge` | Triggers background asynchronous knowledge ingestion |
| `GET` | `/rag/booking-state/{session_id}` | Inspects active slot-filling state for a given session |
| `DELETE`| `/rag/clear-session/{session_id}` | Clears conversation memory buffer |
| `GET` | `/rag/stats` | Retrieves indexed chunk counts, vector dimensions, and latency metrics |
| `GET` | `/health` | Health check & model connectivity status |

---

## 🔒 Security, Performance & Enterprise Guardrails

- **Zero Hardcoded Credentials**: All secrets, API keys, and environment variables are strictly loaded via `.env`.
- **Request DTO Sanitization**: NestJS utilizes `class-validator` to enforce strict types and reject malicious payloads.
- **Enterprise Rate Limiting**: Throttler guards protect against brute-force authentication and AI denial-of-service.
- **Strict Grounding Guardrails**: Zero hallucination tolerance. If vehicle specifications or policies are not in verified context, the model politely defaults to support contact details.
- **CORS & Security Headers**: Helmet middleware enabled to prevent clickjacking, MIME sniffing, and cross-site scripting.

---

## 📁 Repository & Directory Structure

```
backend/
├── ai-service/                   # Python 3.12 FastAPI RAG Microservice
│   ├── app/
│   │   ├── api/                  # REST routes for /rag/chat, /rag/search, /rag/stats
│   │   ├── booking/              # Conversational slot-filling booking engine
│   │   ├── context/              # Context builder, token budgeting, deduplication
│   │   ├── core/                 # App configuration, logging, prompts
│   │   ├── generation/           # LLM generators (Gemini) & grounding validation
│   │   ├── indexing/             # Knowledge base chunking & vector sync
│   │   ├── memory/               # Multi-turn conversation memory buffer
│   │   ├── query/                # Multilingual parser & intent planner
│   │   ├── retrieval/            # Hybrid vector + BM25 retriever & reranker
│   │   └── main.py               # FastAPI application bootstrap
│   ├── tests/                    # Pytest test suite (RAG, Vector, Scorer)
│   ├── Dockerfile
│   └── requirements.txt
│
└── backend-gateway/              # NestJS Core API Gateway
    ├── src/
    │   ├── common/               # Guards, interceptors, filters, decorators
    │   ├── modules/
    │   │   ├── ai-proxy/         # Secure HTTP proxy to FastAPI AI Service
    │   │   ├── analytics/        # Business intelligence & KPI aggregation
    │   │   ├── auth/             # JWT Authentication & RBAC security
    │   │   ├── automation/       # Webhooks & automated lead triggers
    │   │   ├── availability/     # Real-time vehicle scheduling & conflicts
    │   │   ├── bookings/         # Booking lifecycle state machine
    │   │   ├── cars/             # Fleet catalog management
    │   │   ├── payments/         # Payment transactions & billing
    │   │   ├── pricing/          # Dynamic price calculations & discounts
    │   │   ├── reports/          # Admin export & financial summaries
    │   │   ├── reviews/          # Customer feedback & ratings
    │   │   └── vehicles/         # Vehicle specifications & inventory
    │   ├── app.module.ts         # Root NestJS module
    │   └── main.ts               # NestJS bootstrap with Swagger OpenAPI
    ├── test/                     # End-to-end integration tests
    ├── Dockerfile
    └── package.json
```

---

## 🛠️ Step-by-Step Installation & Local Setup

### Prerequisites
- **Node.js**: `v18.x` or `v20.x`+
- **Python**: `v3.11` or `v3.12`+
- **npm** or **pnpm**
- **Docker & Docker Compose** (Optional)

---

### Step 1: Start AI Microservice (FastAPI)

```bash
# Navigate to AI Service directory
cd backend/ai-service

# Create and activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env configuration
cat <<EOF > .env
PORT=8000
HOST=0.0.0.0
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
EMBEDDING_MODEL=models/text-embedding-004
EOF

# Start FastAPI server in reload mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- **Service URL**: `http://localhost:8000`
- **Interactive Swagger Documentation**: `http://localhost:8000/docs`

---

### Step 2: Start API Gateway (NestJS)

```bash
# Open a new terminal and navigate to Gateway directory
cd backend/backend-gateway

# Install dependencies
npm install

# Create .env configuration
cat <<EOF > .env
PORT=3001
AI_SERVICE_URL=http://localhost:8000
JWT_SECRET=your_super_secret_jwt_key_here
JWT_EXPIRES_IN=7d
CORS_ORIGIN=http://localhost:3000
EOF

# Start NestJS in development mode
npm run start:dev
```
- **Gateway URL**: `http://localhost:3001`
- **Swagger OpenAPI Documentation**: `http://localhost:3001/api/docs`

---

## 🐳 Docker & Containerized Deployment

Run both backend microservices with a single command from the project root:

```bash
docker compose up --build
```

---

## 🧪 Testing & Quality Assurance

### Run AI Microservice Tests
```bash
cd backend/ai-service
pytest -v
```

### Run API Gateway Tests
```bash
cd backend/backend-gateway

# Unit tests
npm test

# End-to-end integration tests
npm run test:e2e

# Production build test
npm run build
```

---

## 📄 License

This project is licensed under the MIT License.
