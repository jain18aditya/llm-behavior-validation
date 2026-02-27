
# Week 4 — Production RAG Knowledge Agent

## Overview

This project implements a production-style Retrieval-Augmented Generation (RAG) Knowledge Agent with:

- Persistent vector storage (Chroma)
- Sliding window document chunking
- Hybrid retrieval (vector + keyword search)
- Distance threshold filtering
- LLM-based reranking
- Grounded answer generation
- Source citation
- Retrieval evaluation (Precision@K, Faithfulness)
- Latency and token tracking
- Structured logging
- Basic prompt injection defense

---

## Architecture

User Query
→ Injection Guard
→ Query Embedding
→ Vector Retrieval (Top-K)
→ Distance Threshold Filtering
→ Hybrid Ranking
→ LLM Reranking
→ Context Injection
→ Grounded LLM Generation
→ Evaluation + Logging

---

## Core Features

### Embeddings
Uses `text-embedding-3-small` for semantic vector representation.

### Persistent Vector Database
Chroma PersistentClient with metadata storage for source tracking.

### Chunking
Sliding window chunking with configurable size and overlap.

### Hybrid Search
Final score:
score = alpha * vector_similarity + (1 - alpha) * keyword_overlap

### Reranking
LLM ranks Top-K retrieved chunks and selects Top-N most relevant.

### Grounded Prompting
System + User roles used to enforce strict context-based answering.

### Source Citation
Each chunk includes metadata source. Final answers return used sources.

---

## Evaluation Metrics

- Precision@K (retrieval quality)
- Faithfulness (hallucination detection via LLM judge)
- Latency measurement
- Token usage tracking

---

## Observability

Structured JSON logging includes:
- Retrieval distances
- Precision
- Faithfulness
- Latency
- Token usage
- Sources used

---

## How to Run

1. Install dependencies
2. Configure OpenAI API key
3. Run:

python week4_rag_production.py

---

## Interview Summary

Built a production-grade RAG system with hybrid retrieval, reranking, grounded generation, evaluation metrics, observability, and injection defense.

