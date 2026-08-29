# RAG Architecture Plan
## Production-Grade Agentic RAG Module

### 1. Objective

Build a production-grade, database-driven, multilingual, agentic RAG module for the car rental platform.

The RAG system must:

- Use PostgreSQL as the single source of truth.
- Never depend on hardcoded/static business knowledge.
- Automatically create/update embeddings when database data is inserted or modified.
- Perform embedding/indexing asynchronously in background workers.
- Never block or slow down other users' queries because of embedding operations.
- Use pre-generated document/entity embeddings during retrieval.
- Generate only the user query embedding at query time.
- Support Bangla, English, Banglish, and mixed-language queries.
- Support semantic, keyword, and hybrid retrieval.
- Support metadata filtering.
- Support reranking.
- Support query rewriting and adaptive retrieval.
- Support persistent conversation memory.
- Support user-specific long-term memory.
- Support agentic multi-step retrieval.
- Detect insufficient context and perform additional retrieval when necessary.
- Maintain embedding versioning and index consistency.
- Provide observability, retries, failure handling, and retrieval evaluation.

---

# 2. High-Level Architecture

```text
                              ┌──────────────────────┐
                              │       AI AGENT       │
                              │                      │
                              │ Planning             │
                              │ Tool Calling         │
                              │ Reasoning            │
                              └──────────┬───────────┘
                                         │
                                         ▼
                         ┌────────────────────────────┐
                         │      RAG ORCHESTRATOR      │
                         │                            │
                         │ Query Analysis             │
                         │ Language Detection         │
                         │ Intent Detection           │
                         │ Query Rewriting            │
                         │ Retrieval Planning          │
                         │ Retrieval Strategy         │
                         └─────────────┬──────────────┘
                                       │
                  ┌────────────────────┼────────────────────┐
                  │                    │                    │
                  ▼                    ▼                    ▼
          ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
          │    Memory    │     │  Semantic    │     │   Keyword    │
          │  Retrieval   │     │  Retrieval   │     │  Retrieval   │
          └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
                 │                    │                    │
                 │                    ▼                    │
                 │             ┌──────────────┐            │
                 │             │   pgvector   │            │
                 │             │              │            │
                 │             │ Embeddings   │            │
                 │             │ Metadata     │            │
                 │             └──────┬───────┘            │
                 │                    │                    │
                 └────────────────────┼────────────────────┘
                                      ▼
                              ┌──────────────┐
                              │ Hybrid Fusion│
                              │     RRF      │
                              └──────┬───────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │   Reranker   │
                              └──────┬───────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │ Context Builder │
                            │                 │
                            │ Deduplication   │
                            │ Compression     │
                            │ Token Budget    │
                            └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │ Grounding Check │
                            └────────┬────────┘
                                     │
                            ┌────────┴────────┐
                            │                 │
                          Enough            Not enough
                            │                 │
                            ▼                 ▼
                           LLM          Query Rewriting
                                             │
                                             ▼
                                      Re-retrieval Loop
```

---

# 3. Core Components

```text
rag/
│
├── orchestrator/
│   ├── rag-orchestrator
│   ├── query-analyzer
│   ├── retrieval-planner
│   └── retrieval-router
│
├── query/
│   ├── language-detector
│   ├── normalizer
│   ├── query-rewriter
│   ├── intent-detector
│   └── entity-extractor
│
├── retrieval/
│   ├── semantic-retriever
│   ├── keyword-retriever
│   ├── hybrid-retriever
│   ├── metadata-filter
│   ├── memory-retriever
│   └── adaptive-retriever
│
├── ranking/
│   ├── reranker
│   ├── score-fusion
│   └── relevance-filter
│
├── context/
│   ├── context-builder
│   ├── deduplicator
│   ├── compressor
│   └── token-budget-manager
│
├── grounding/
│   ├── grounding-checker
│   ├── evidence-validator
│   └── confidence-estimator
│
├── memory/
│   ├── conversation-memory
│   ├── user-memory
│   ├── memory-extractor
│   └── memory-retriever
│
├── indexing/
│   ├── change-detector
│   ├── document-builder
│   ├── chunker
│   ├── embedding-service
│   ├── index-updater
│   └── index-version-manager
│
├── workers/
│   ├── embedding-worker
│   ├── reindex-worker
│   └── cleanup-worker
│
├── queue/
│   ├── embedding-queue
│   ├── reindex-queue
│   └── retry-manager
│
└── evaluation/
    ├── retrieval-evaluator
    ├── relevance-evaluator
    └── metrics
```

---

# 4. Database Architecture

PostgreSQL is the primary source of truth.

Use PostgreSQL with the `pgvector` extension.

### Business Data

```text
users
vehicles
vehicle_categories
locations
bookings
payments
pricing_rules
reviews
maintenance
policies
faqs
...
```

### RAG Data

```text
rag_documents
rag_chunks
rag_embeddings
rag_metadata
embedding_jobs
embedding_versions
```

### Memory Data

```text
conversations
messages
user_memories
conversation_summaries
memory_embeddings
```

---

# 5. RAG Document Representation

Every searchable database entity must be converted into a canonical textual representation.

Example:

```text
Vehicle:

Toyota Premio 2022.
Vehicle type: Sedan.
Seats: 5.
Transmission: Automatic.
Fuel type: Petrol.
Location: Dhaka.
Daily rental price: 5000 BDT.
Current status: Available.
```

This canonical representation becomes the source for chunking and embedding.

Do not maintain separate hardcoded knowledge for vehicles, pricing, policies, or availability.

---

# 6. Automatic Database-to-Embedding Pipeline

```text
                PostgreSQL
                    │
              INSERT / UPDATE
                    │
                    ▼
             Change Detection
                    │
              Content Hash
                    │
             ┌──────┴──────┐
             │             │
          Changed       Unchanged
             │             │
             ▼             └──► Ignore
          Event
             │
             ▼
       Embedding Queue
             │
             ▼
      Background Worker
             │
             ▼
     Canonical Text Builder
             │
             ▼
          Chunking
             │
             ▼
   Multilingual Embedding Model
             │
             ▼
         pgvector
```

Embedding generation must never be performed synchronously inside the user's API request.

---

# 7. Non-Blocking Embedding Strategy

Embedding operations must run independently from user requests.

Recommended architecture:

```text
                    PostgreSQL
                        │
                        ▼
                  Change Event
                        │
                        ▼
                  Redis Queue
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
        Worker 1     Worker 2     Worker 3
            │           │           │
            └───────────┼───────────┘
                        ▼
                 Embedding Service
                        │
                        ▼
                    pgvector
```

Requirements:

- Asynchronous processing.
- Multiple workers.
- Retry failed jobs.
- Exponential backoff.
- Dead-letter queue for permanently failed jobs.
- Job deduplication.
- Update coalescing/debouncing.
- Batch embedding when appropriate.
- No database-wide locks during embedding.
- No user request should wait for embedding completion.

---

# 8. Query-Time Retrieval

The system must NOT re-embed database documents at query time.

Only the user query is embedded at runtime.

```text
User Query
    │
    ▼
Language Detection
    │
    ▼
Query Normalization
    │
    ▼
Intent Detection
    │
    ▼
Query Rewriting
    │
    ▼
Query Embedding
    │
    ├───────────────┐
    ▼               ▼
Semantic Search   Keyword Search
    │               │
    └───────┬───────┘
            ▼
       Hybrid Fusion
            │
            ▼
         Reranking
            │
            ▼
       Context Builder
```

---

# 9. Multilingual Retrieval

The RAG system must support:

```text
English
Bangla
Banglish
English + Bangla
English + Banglish
Bangla + English
```

Examples:

```text
"Which SUV is available in Dhaka?"

"ঢাকায় কোন SUV available?"

"Dhaka te kon SUV available?"

"amar family er jonno comfortable gari lagbe"
```

All queries should be processed through the same multilingual retrieval pipeline.

Use a multilingual embedding model capable of handling Bangla and English semantic similarity.

Do not rely only on exact string matching.

---

# 10. Hybrid Retrieval

Use both:

```text
Semantic Search
+
PostgreSQL Full Text / Keyword Search
```

Then combine results using Reciprocal Rank Fusion (RRF) or another configurable score-fusion strategy.

```text
                Query
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
  Vector Search        Keyword Search
   pgvector              PostgreSQL
        │                   │
        └─────────┬─────────┘
                  ▼
             RRF Fusion
                  │
                  ▼
           Candidate Set
```

Semantic search handles conceptual queries.

Keyword search handles:

- Exact vehicle names.
- Model numbers.
- Locations.
- Booking IDs.
- Policy names.
- Specific terms.

---

# 11. Metadata Filtering

Retrieval must support structured metadata filters.

Example:

```text
location = Dhaka
vehicle_type = SUV
transmission = automatic
seats >= 5
price_per_day <= 6000
status = available
```

The retrieval planner should extract applicable filters from the query before performing retrieval.

Example:

```text
"Dhaka te 6000 takar moddhe automatic SUV chai"

↓

location = Dhaka
vehicle_type = SUV
transmission = automatic
max_price = 6000
```

Metadata filtering must be combined with semantic retrieval.

---

# 12. Reranking

Initial retrieval may return 20–50 candidates.

Use a reranker to reduce this to the most relevant context.

```text
Vector + Keyword Retrieval
          │
          ▼
     Top 30 Candidates
          │
          ▼
        Reranker
          │
          ▼
       Top 5–10
```

Reranking should consider:

- Semantic relevance.
- Query intent.
- Metadata match.
- User context.
- Freshness.
- Entity relevance.

---

# 13. Adaptive Retrieval

Do not assume that one retrieval operation is always sufficient.

```text
Query
 ↓
Retrieve
 ↓
Rerank
 ↓
Grounding Check
 ↓
Enough evidence?
 │
 ├── YES → Context → LLM
 │
 └── NO
       ↓
   Query Rewrite
       ↓
   Additional Retrieval
       ↓
   Rerank
       ↓
   Grounding Check
```

Set a maximum retrieval iteration limit to prevent infinite loops.

Example:

```text
MAX_RETRIEVAL_ITERATIONS = 2 or 3
```

---

# 14. Agentic RAG

The RAG module must expose retrieval capabilities as tools that the AI agent can call.

Example tools:

```text
search_knowledge()
search_vehicles()
search_policies()
search_locations()
search_faq()
search_user_memory()
search_conversation()
```

The agent decides which retrieval operation is required.

Example:

```text
User:
"Dhaka te family er jonno 5000 takar moddhe automatic car ache?"

Agent:
  1. Extract constraints.
  2. Search vehicle knowledge.
  3. Apply metadata filters.
  4. Check relevant live information through the appropriate business tool.
  5. Retrieve supporting knowledge if required.
  6. Rerank.
  7. Generate answer.
```

The RAG module should not independently perform business transactions.

---

# 15. Memory Architecture

Memory must be separated from general knowledge retrieval.

```text
                    Query
                      │
             ┌────────┴────────┐
             ▼                 ▼
       Knowledge RAG       Memory RAG
             │                 │
             ▼                 ▼
         pgvector           pgvector
```

### Short-Term Memory

Current conversation:

```text
conversation_id
message history
current intent
current entities
current constraints
```

### Long-Term Memory

Useful user preferences:

```text
preferred_vehicle_type
preferred_transmission
preferred_location
usual_rental_duration
important_preferences
```

### Conversation Summary

Long conversations should be summarized to avoid sending the complete history to the LLM.

---

# 16. Memory Extraction

Do not save every conversation message as permanent memory.

The memory layer should determine whether information is:

```text
Temporary Context
        OR
Long-Term Memory
```

Example:

```text
"I need an SUV today."

→ temporary context

"I usually prefer automatic SUVs."

→ long-term preference
```

Memory should have:

```text
importance
confidence
source
created_at
updated_at
```

---

# 17. Context Assembly

Retrieved information must pass through a context builder.

```text
Retrieved Results
      │
      ▼
Deduplication
      │
      ▼
Relevance Filtering
      │
      ▼
Freshness Filtering
      │
      ▼
Context Compression
      │
      ▼
Token Budget
      │
      ▼
Final Context
```

Never send every retrieved document directly to the LLM.

---

# 18. Grounding and Confidence

Before generating the final response:

```text
Retrieved Context
       │
       ▼
Evidence Validation
       │
       ▼
Confidence Check
```

If sufficient evidence is unavailable:

```text
Do not hallucinate.
Do not invent business information.
Perform additional retrieval or clearly state that sufficient information is unavailable.
```

---

# 19. Data Freshness

Every embedding record must contain:

```text
entity_id
entity_type
content_hash
embedding_model
embedding_version
source_version
created_at
updated_at
embedded_at
status
```

Example:

```text
vehicle_id = 101
source_version = 8
embedding_version = 3
status = ACTIVE
```

The retrieval system must prefer the current active embedding version.

---

# 20. Incremental Indexing

Never re-embed the entire database when one record changes.

```text
1 vehicle changed
       ↓
1 embedding job
       ↓
1 vector update
```

For repeated updates:

```text
UPDATE
UPDATE
UPDATE
UPDATE

       ↓

Coalesce/Debounce

       ↓

One final embedding job
```

This reduces:

- Embedding cost.
- Queue pressure.
- Worker load.
- Database writes.

---

# 21. Atomic Index Update

When a new embedding is generated:

```text
Old Embedding
     │
     │
New Embedding generated
     │
     ▼
Validate
     │
     ▼
Atomic activation
     │
     ▼
New Embedding = ACTIVE
Old Embedding = INACTIVE
```

Never expose partially generated or invalid embeddings to retrieval.

---

# 22. Embedding Version Management

Support multiple embedding versions.

```text
Embedding Model V1
Embedding Model V2
Embedding Model V3
```

Migration flow:

```text
V1 ACTIVE
   ↓
Generate V2 in background
   ↓
Validate V2
   ↓
V2 ACTIVE
   ↓
V1 DEPRECATED
```

This allows embedding-model upgrades without downtime.

---

# 23. Failure Handling

Embedding jobs must support:

```text
PENDING
PROCESSING
COMPLETED
FAILED
RETRYING
DEAD_LETTER
```

Retry strategy:

```text
Attempt 1
   ↓
Failure
   ↓
Backoff
   ↓
Attempt 2
   ↓
Failure
   ↓
Backoff
   ↓
Attempt 3
   ↓
Dead Letter Queue
```

A failed embedding job must not block other jobs.

---

# 24. Caching

Cache where appropriate:

```text
Query normalization
Frequent retrieval results
Frequently accessed knowledge
Conversation summaries
```

Do not cache highly dynamic information such as:

```text
vehicle availability
booking status
payment status
```

unless the cache has strict invalidation rules.

---

# 25. Observability

Track every retrieval request.

Minimum telemetry:

```text
request_id
user_id
conversation_id

original_query
normalized_query
language
intent

retrieval_strategy

semantic_results_count
keyword_results_count
final_results_count

reranker_scores

retrieval_latency
embedding_latency
reranking_latency
LLM_latency

token_usage

grounding_score
confidence_score

cache_hit
retrieval_iterations

errors
```

This is required for production debugging and RAG evaluation.

---

# 26. RAG Evaluation

Maintain an evaluation dataset containing real user queries in:

```text
English
Bangla
Banglish
Mixed language
```

Evaluate:

```text
Recall@K
Precision@K
MRR
NDCG
Retrieval relevance
Grounding
Answer faithfulness
Latency
```

Example:

```text
Query:
"Dhaka te family er jonno automatic gari chai"

Expected:
Relevant automatic family vehicles in Dhaka

Evaluate:
Did retrieval return the correct entities?
```

---

# 27. Security Rules

The RAG system must respect user authorization.

Never retrieve data that the current user is not allowed to access.

Apply authorization filters before context reaches the LLM.

```text
User
 ↓
Authorization
 ↓
Metadata Filter
 ↓
Retrieval
 ↓
Reranking
 ↓
Context
```

Sensitive business/customer data must never leak through semantic retrieval.

---

# 28. Source Priority

When multiple information sources exist, use this priority:

```text
1. Current PostgreSQL business data
2. Current indexed RAG representation
3. User-specific memory
4. Historical conversation context
5. General model knowledge
```

The LLM must never override current database facts with its pretrained knowledge.

For dynamic business facts, PostgreSQL/business APIs remain authoritative.

---

# 29. Final Retrieval Pipeline

```text
USER QUERY
    │
    ▼
Query Analyzer
    │
    ├── Language
    ├── Intent
    ├── Entities
    └── Constraints
    │
    ▼
Query Rewriter
    │
    ▼
Retrieval Planner
    │
    ├──────────────┬──────────────┐
    ▼              ▼              ▼
 Memory        Semantic        Keyword
 Retrieval     Retrieval       Retrieval
    │              │              │
    │              ▼              │
    │          pgvector            │
    │              │              │
    └──────────────┼──────────────┘
                   ▼
             Hybrid Fusion
                   │
                   ▼
               Reranker
                   │
                   ▼
            Freshness Filter
                   │
                   ▼
             Deduplication
                   │
                   ▼
          Context Compression
                   │
                   ▼
            Token Management
                   │
                   ▼
           Grounding Check
                   │
             ┌─────┴─────┐
             │           │
          Sufficient   Insufficient
             │           │
             ▼           ▼
            LLM      Query Rewrite
                         │
                         ▼
                   Re-retrieval
```

---

# 30. Background Indexing Pipeline

```text
DATABASE
   │
   │ INSERT / UPDATE / DELETE
   ▼
Change Detection
   │
   ▼
Content Hash
   │
   ├── No Change ──────────────► Ignore
   │
   ▼
Event
   │
   ▼
Redis / Queue
   │
   ▼
Embedding Worker Pool
   │
   ├── Fetch Current DB Data
   ├── Build Canonical Representation
   ├── Chunk
   ├── Generate Embedding
   ├── Validate
   └── Update pgvector
             │
             ▼
        Mark ACTIVE
```

---

# 31. Important Architectural Rules

### Rule 1

PostgreSQL is the source of truth.

### Rule 2

pgvector is a retrieval index, not the source of truth.

### Rule 3

Never hardcode business data inside the RAG module.

### Rule 4

Never synchronously generate document embeddings inside user requests.

### Rule 5

Only user-query embeddings are generated during normal retrieval.

### Rule 6

Database changes must trigger asynchronous incremental re-indexing.

### Rule 7

Use hybrid retrieval instead of vector-only retrieval.

### Rule 8

Use metadata filtering before/alongside semantic retrieval.

### Rule 9

Use reranking before context construction.

### Rule 10

Use adaptive retrieval when evidence is insufficient.

### Rule 11

Keep memory separate from general knowledge.

### Rule 12

Do not use RAG as the authoritative source for highly dynamic transactional data.

### Rule 13

All retrieval must respect authorization.

### Rule 14

All embeddings must be versioned.

### Rule 15

All retrieval operations must be observable and measurable.

---

# 32. Recommended RAG Stack

```text
Database
    PostgreSQL

Vector Search
    pgvector

Keyword Search
    PostgreSQL Full Text Search

Queue
    Redis

Background Workers
    Python workers / dedicated embedding workers

AI/RAG Service
    Python + FastAPI

Agent Integration
    Tool-based Agentic RAG

Embedding
    Multilingual embedding model
    (Bangla + English capable)

Reranking
    Multilingual / cross-encoder reranker

Memory
    PostgreSQL + pgvector

Caching
    Redis

Monitoring
    Structured logs + metrics + tracing
```

---

# 33. Target Architecture Principle

The final system should behave like this:

```text
                    ┌──────────────────┐
                    │    PostgreSQL    │
                    │                  │
                    │  SOURCE OF TRUTH │
                    └────────┬─────────┘
                             │
                     Async Indexing
                             │
                             ▼
                    ┌──────────────────┐
                    │     pgvector     │
                    │                  │
                    │ RETRIEVAL INDEX  │
                    └────────┬─────────┘
                             │
                             ▼
                       RAG ENGINE
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
       Memory            Knowledge          Retrieval
       Search              Search             Tools
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ▼
                       AI AGENT
                             │
                             ▼
                            LLM
```

The RAG module must therefore be treated as a **continuously synchronized retrieval layer over PostgreSQL**, not as a static document chatbot.

The system should always prioritize **fresh, authorized, database-backed evidence**, while using semantic retrieval, hybrid search, reranking, memory, and adaptive agentic retrieval to produce natural responses across Bangla, Banglish, and English.