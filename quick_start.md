# LLM Call Center Analytics on Databricks

Build a Sales Coach that helps Representatives improve using LLM analysis of call transcripts.

## Quick Start

### Option 1: Import via Databricks Repos

1. In your Databricks workspace, go to Repos
2. Click "Add Repo"
3. Enter this repository URL: `https://github.com/brij-raghuwanshi-db/llm-call-center-analytics`
4. Click "Create"

### Option 2: Run Individual Notebooks

1. Download the notebooks from this repository
2. Import them into your Databricks workspace:
   - Workspace → Click menu (⋮) → Import
   - Select the downloaded notebook files

## Prerequisites

- Databricks workspace with Unity Catalog enabled
- Access to Foundation Model APIs (`databricks-gte-large-en` and `databricks-claude-3-7-sonnet`)
- Vector Search endpoint available in your workspace region

## Setup

1. Install dependencies:
```python
%pip install -r requirements.txt
```

2. Configure workspace parameters in `000_initialize`:
```python
catalog_name = 'your_catalog'  # Unity Catalog name
schema_name = 'your_schema'    # Schema name
```

3. Run notebooks in sequence:
- `000_initialize.py`: Setup workspace paths and parameters
- `001_get_data.py`: Load and process transcripts
- `002_create_vector_search_index.py`: Create embeddings and search index
- `003_RAG.py`: Deploy RAG chain for insights

## Features

- **Participant Assessment**: Extract structured insights about each participant using `ai_query`
- **Vector Search**: Find similar conversations and patterns
- **RAG Chatbot**: Ask questions about participant performance
- **MLflow Integration**: Track and deploy LangChain models

## Screenshots

See `screenshots/` directory for step-by-step visuals of:
- Raw to structured data transformation
- AI-assisted participant assessments
- Vector search and RAG responses

## Architecture

1. **Data Processing**:
   - Load JSON transcripts
   - Clean and structure conversations
   - Generate participant assessments via `ai_query`

2. **Vector Search**:
   - Create embeddings (GTE-large)
   - Build search index
   - Enable similarity search

3. **RAG Pipeline**:
   - Configure LangChain components
   - Log chain with MLflow
   - Deploy with Databricks Agents

## Dependencies

See `requirements.txt` for full list. Key packages:
- `databricks-langchain`
- `databricks-vectorsearch`
- `databricks-agents`

## Documentation Links

- [Databricks AI Functions](https://docs.databricks.com/en/large-language-models/ai-functions.html)
- [Vector Search](https://docs.databricks.com/en/generative-ai/vector-search/index.html)
- [Foundation Models](https://docs.databricks.com/en/generative-ai/foundation-models/index.html)
- [MLflow](https://docs.databricks.com/en/machine-learning/mlflow/index.html)
- [Unity Catalog](https://docs.databricks.com/en/data-governance/unity-catalog/index.html)