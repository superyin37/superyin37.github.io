# Kitakyushu City Smart Waste Sorting System  
**Interview Project Introduction**

## Project Overview

**Project Name**: Kita – Kitakyushu City Smart Waste Sorting Q&A System  
**Project Type**: RAG (Retrieval-Augmented Generation) Question Answering System  
**Development Period**: GMO Internship Project  
**Team Size**: 3 members (Sota Aoki, Hanyang Yin, Taro Yasuda)  
**My Role**: [Please describe your specific role and responsibilities]

---

## Background and Objectives

### Business Challenges
- Waste sorting rules in Kitakyushu City are complex, making it difficult for users to quickly obtain accurate information
- Garbage collection days differ by neighborhood, making searches inconvenient
- Existing search methods are inefficient and provide a poor user experience

### Solution
We developed a smart Q&A system based on a RAG architecture that provides the following through natural language interaction:
- Search for waste sorting rules
- Lookup of garbage collection days by town name
- Extensible custom knowledge base functionality

---

## System Architecture Design

### Technology Stack Selection

**Frontend Layer**
- **Streamlit**: Rapid development of an interactive web UI
- **GPU Monitoring**: Real-time resource usage display via NVML / nvidia-smi

**Backend Layer**
- **FastAPI**: Asynchronous API framework supporting high concurrency
- **RESTful APIs**: Dual response modes (blocking / streaming)

**Core RAG Engine**
- **ChromaDB**: Vector database supporting efficient semantic search
- **MeCab**: Japanese morphological analysis
- **Hybrid Grounding System v2.0**: In-house intelligent item name recognition system

**LLM Inference**
- **Ollama**: Local deployment ensuring data privacy
- **Llama-3.1-Swallow-8B**: Japanese-optimized large language model
- **cl-nagoya-ruri-large**: Japanese embedding model

### Architecture Highlights

```

User Input → Hybrid Grounding → ChromaDB Search → RAG Prompt → LLM Generation → Response
(Smart Recognition)   (Multi-source Retrieval)                (Streaming / Blocking)

````

**Three-layer Architecture**:
1. **Presentation Layer** (Streamlit): Chat UI, logs display, file upload
2. **Business Layer** (FastAPI): API routing, RAG orchestration, data validation
3. **Data Layer** (ChromaDB): Waste rules, area information, user knowledge base

---

## Core Technical Innovations

### 1. Hybrid Grounding System v2.0 (Key Technology)

**Problem**: Traditional MeCab tokenization lacks accuracy for complex queries

**Innovative Solution**: A three-layer intelligent recognition system

#### Layer 1: Exact Match
- Full match with database → confidence 1.0 → immediate response
- Response time < 5 ms

#### Layer 2: Smart Routing (Path Selection)
```python
if input_length < 20:
    → Path A (Fast Path): Global embedding search
    → Response time < 300 ms
else:
    → Path A + Path B (Dual Path):
       - Path A: Global semantic search
       - Path B: LLM-assisted phrase extraction + segmented search
    → Response time < 600 ms
````

#### Layer 3: Confidence Evaluation

* **High** (≥ 0.70): Direct adoption
* **Medium** (0.45–0.70): Presented to user
* **Low** (< 0.45): Automatic fallback to MeCab

#### Results

* Accuracy improvement: 78% → 92%
* Average response time: < 400 ms
* Automatic fault tolerance via fallback mechanisms

---

### 2. Streaming Response Optimization

**Problem**: Blocking responses caused long wait times and poor UX

**Solution**:

* Implemented Server-Sent Events (SSE) for streaming responses
* Token-by-token output with Time to First Byte (TTFB) < 1s
* Real-time frontend rendering, significantly reducing perceived latency

---

### 3. Multi-source Knowledge Base Integration

**Three independent ChromaDB collections**:

1. **gomi**: Waste sorting rules (static data)
2. **area**: Town-based collection schedules (static data)
3. **knowledge**: User-uploaded knowledge (dynamic extension)

**Benefits**:

* Higher retrieval accuracy through specialization
* Support for hot updates of knowledge bases
* Easier access control and version management

---

## Implementation Details

### RAG Pipeline Walkthrough

```python
# 1. Query understanding
query = "I want to dispose of a laptop"

# 2. Item extraction via Hybrid Grounding
result = hybrid_grounding.extract(query)
# → primary_candidate: "laptop"
# → confidence: "high" (0.98)
# → execution_time: 35ms

# 3. Multi-source retrieval
gomi_docs = chroma_gomi.query(embedding(candidate_item), k=3)
area_docs = chroma_area.query(embedding(town_name), k=2)
knowledge_docs = chroma_knowledge.query(embedding(query), k=2)

# 4. Context construction
context = format_rag_prompt(gomi_docs, area_docs, knowledge_docs)

# 5. LLM generation
response = ollama.generate(
    model="swallow:latest",
    prompt=context + query,
    stream=True  # streaming response
)
```

### Data Structure Design

**ChromaDB Collection Schema**:

```python
# gomi collection
{
    "id": "gomi_001",
    "document": "Please dispose of laptops as bulky waste...",
    "metadata": {
        "item_name": "laptop",
        "category": "bulky waste",
        "source_file": "gomi_rules.pdf",
        "page": 15
    }
}

# area collection
{
    "id": "area_001",
    "document": "Household waste in Yahatahigashi Ward is collected on Mondays and Thursdays...",
    "metadata": {
        "town": "Yahatahigashi Ward",
        "waste_type": "household waste",
        "collection_days": ["Mon", "Thu"]
    }
}
```

### API Design

**Blocking Mode** – POST `/api/bot/respond`

```json
{
  "message": "I want to dispose of a laptop",
  "user_id": "user123",
  "stream": false
}
```

**Streaming Mode** – POST `/api/bot/respond_stream`

```
data: {"type": "token", "content": "laptop"}
...
data: {"type": "done", "references": [...]}
```

---

## Performance Metrics

### Response Performance

* **TTFB (Time to First Byte)**: 800 ms
* **Full Response Time**: 3–5 seconds (depending on answer length)
* **Hybrid Grounding**: 35–600 ms
* **ChromaDB Retrieval**: 50–150 ms

### Accuracy Metrics

* **Item Recognition Accuracy**: 92% (vs. MeCab 78%)
* **Waste Rule Accuracy**: 96%
* **Area Information Accuracy**: 99% (structured data)

### System Resources

* **VRAM Usage**: 6–8 GB (8B model)
* **CPU Usage**: 20–40%
* **Memory Usage**: 4–6 GB

---

## Development Process and Challenges

### Challenge 1: Low Accuracy in Japanese Item Name Extraction

**Issue**:

* MeCab tokenization struggles with long sentences and compound nouns
* Example: “使わなくなったノートパソコン” → extraction failure

**Resolution**:

1. Evaluated existing NER solutions → unsuitable for waste-sorting domain
2. Tested pure embedding-based search → effective for short phrases only
3. Designed a hybrid solution combining global search and LLM extraction
4. Implemented automatic fallback for robustness

**Result**: Accuracy improved from 78% to 92%

---

### Challenge 2: Choppy Streaming Responses

**Issue**: Frontend rendering lag and token accumulation

**Solution**:

* Tuned backend buffer size
* Implemented asynchronous updates using `useEffect` + `useState`
* Added heartbeat detection mechanism

---

### Challenge 3: ChromaDB Performance Optimization

**Optimizations**:

1. Separated collections (gomi / area / knowledge)
2. Tuned `n_results` parameter (3–5)
3. Applied metadata filtering to remove irrelevant results
4. Enabled persistence mode to avoid reload overhead

---

## Key Learnings

### Technical Growth

1. **RAG Architecture**: Deep understanding from theory to production
2. **Vector Databases**: Mastery of ChromaDB usage and optimization
3. **LLM Applications**: Prompt engineering and streaming implementation
4. **Full-stack Development**: End-to-end FastAPI backend and Streamlit frontend
5. **Performance Optimization**: Bottleneck identification, metrics-driven iteration

### Engineering Skills

1. **System Design**: Modular design, layered architecture, interface definition
2. **Code Quality**: Pydantic validation, type hints, exception handling
3. **Documentation**: Architecture docs, API docs, README authoring
4. **Team Collaboration**: Git-based version control, code reviews, task allocation

### Business Understanding

1. **Requirement Analysis**: Designing solutions from real user pain points
2. **User Experience**: Streaming responses, confidence indicators, transparent logs
3. **Scalability**: Support for user-uploaded knowledge and continuous iteration

---
