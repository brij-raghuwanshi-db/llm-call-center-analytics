# Sales Coaching on Databricks: Architecture Diagram Specifications

## Layer-by-Layer Architecture Breakdown

### 1. DATA FOUNDATION LAYER
```
┌─────────────────────────────────────────────────────────┐
│                    UNITY CATALOG                        │
├─────────────────────────────────────────────────────────┤
│  📁 /Volumes/users/schema/conversation_demo_data/       │
│     ├── anonymized_conversation_data.json               │
│     ├── conversation_001.json                           │
│     └── conversation_N.json                             │
│                                                         │
│  📊 Delta Tables:                                       │
│     ├── conversation_demo                               │
│     ├── conversation_participant_summary                │
│     └── each_participant_summary                        │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
```

### 2. AI PROCESSING LAYER
```
┌─────────────────────────────────────────────────────────┐
│                   SPARK + AI FUNCTIONS                  │
├─────────────────────────────────────────────────────────┤
│  🔄 Data Preprocessing:                                 │
│     • JSON parsing with pandas_udf                      │
│     • Sentence attribution to participants              │
│     • Conversation structuring                          │
│                                                         │
│  🧠 AI Functions (ai_query):                            │
│     • Model: databricks-claude-3-7-sonnet               │
│     • JSON Schema Validation                            │
│     • Automated PII Masking                             │
│     • Participant Performance Assessment                │
│                                                         │
│  📋 Structured Outputs:                                 │
│     • Performance metrics, Sales skills                 │
│     • Customer focus, Platform expertise                │
│     • Recommendations, Impact assessment                │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
```

### 3. VECTOR SEARCH LAYER (Dual Path Architecture)
```
           ┌─────────────────────┐      ┌─────────────────────┐
           │    PATTERN 1:       │      │    PATTERN 2:       │
           │  PRE-COMPUTED       │      │   DELTA SYNC        │
           │   EMBEDDINGS        │      │     INDEX           │
           ├─────────────────────┤      ├─────────────────────┤
           │ @pandas_udf         │      │ Auto-embeddings via │
           │ get_embedding()     │      │ databricks-gte-     │
           │                     │      │ large-en endpoint   │
           │ ↓                   │      │ ↓                   │
           │ Structured Streaming│      │ Change Data Feed    │
           │ with embeddings     │      │ synchronization     │
           │ ↓                   │      │ ↓                   │
           │ Delta Table with    │      │ Direct table        │
           │ embedding column    │      │ indexing            │
           └─────────────────────┘      └─────────────────────┘
                         │                        │
                         └────────┬───────────────┘
                                  ▼
           ┌─────────────────────────────────────────────┐
           │         VECTOR SEARCH INDEX                 │
           │  • Hybrid search (semantic + keyword)       │
           │  • Embedding dimension: 1024                │
           │  • Pipeline: TRIGGERED                      │
           │  • Primary key: id/conversation_id          │
           └─────────────────────────────────────────────┘
                                  │
                                  ▼
```

### 4. RAG APPLICATION LAYER
```
┌─────────────────────────────────────────────────────────┐
│                    RAG PIPELINE                         │
├─────────────────────────────────────────────────────────┤
│  🔍 Retrieval Components:                               │
│     • DatabricksVectorSearch as retriever               │
│     • DatabricksEmbeddings for query encoding           │
│     • Hybrid similarity search (k=10)                   │
│                                                         │
│  🧠 Generation Components:                              │
│     • ChatDatabricks (databricks-claude-3-7-sonnet)     │
│     • Conversation history management                   │
│     • Query rewriting for better retrieval              │
│                                                         │
│  🔗 LangChain Integration:                              │
│     • RunnableBranch for conditional logic              │
│     • Context formatting and prompt templates           │
│     • Source attribution and traceability               │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
```

### 5. DEPLOYMENT LAYER
```
┌─────────────────────────────────────────────────────────┐
│                 MLFLOW & DEPLOYMENT                     │
├─────────────────────────────────────────────────────────┤
│  📊 MLflow Tracking & Registry:                         │
│     • Experiment logging with dependencies              │
│     • Model versioning in Unity Catalog                 │
│     • Resource tracking (endpoints, indexes)            │
│                                                         │
│  🚀 Databricks Agents Deployment:                       │
│     • Auto-scaling serving endpoint                     │
│     • Scale-to-zero cost optimization                   │
│     • REST API for external integration                 │
│     • Review App for testing and evaluation             │
│                                                         │
│  🔐 Enterprise Features:                                │
│     • Unity Catalog governance                          │
│     • Audit logging and lineage                         │
│     • Permission management                             │
└─────────────────────────────────────────────────────────┘
```

---

## Key Technical Specifications

### Foundation Models Used:
- **Embeddings**: `databricks-gte-large-en` (1024 dimensions)
- **Chat/Generation**: `databricks-claude-3-7-sonnet`
- **AI Functions**: In-SQL LLM calls with JSON schema validation

### Data Governance:
- **Unity Catalog**: Tables, volumes, permissions, lineage
- **PII Masking**: Automated in AI Functions step
- **Change Data Feed**: Real-time synchronization
- **Schema Evolution**: Automatic handling with mergeSchema

### Production Features:
- **Auto-scaling**: Including scale-to-zero capability
- **A/B Testing**: Model version comparison
- **Monitoring**: Built-in metrics and alerting
- **APIs**: REST endpoints for integration
- **Review App**: Testing and evaluation interface

---

## Data Flow Summary

```
Raw Conversations → Spark Processing → AI Functions → Structured Assessments
                                                           ↓
Vector Search Index ← Embeddings Generation ← Participant Data
       ↓
RAG Pipeline (Retrieval + Generation) ← User Query
       ↓
MLflow Registry → Agents Deployment → Production API
```

## Business Value Proposition

**Input**: Unstructured conversation transcripts
**Process**: Automated AI-powered analysis with governance
**Output**: Actionable coaching insights via natural language interface
**Impact**: 95% time reduction, consistent evaluation, real-time insights