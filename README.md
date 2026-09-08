# RAG Evaluation & Retrieval Benchmark

A small end-to-end Retrieval-Augmented Generation (RAG) system with an
evaluation harness for measuring retrieval quality, answer faithfulness, and
answer correctness across multiple pipeline configurations.

The project uses a domain-specific badminton computer-vision corpus and
focuses on an important RAG engineering problem:

> How do we know whether a change to the retrieval pipeline actually improves
> the quality of the final answers?

---

## 1. Project Overview

The system contains:

- 17 badminton computer-vision documents
- 16 evaluation questions
- Configurable chunk size, overlap, top-k, and embedding model
- ChromaDB vector retrieval
- Gemini-based answer generation
- Source-level retrieval evaluation
- Ragas-inspired context evaluation
- LLM-based faithfulness and correctness evaluation
- Automated comparison across configurations
- Google Sheets + Apps Script evaluation dashboard

The evaluation set includes:

- Single-hop questions
- Paraphrased questions
- Comparative questions
- Multi-hop questions
- Conditional questions
- Abstract questions
- Counterfactual questions

The goal is to separate retrieval failures from generation failures and
measure the effect of different RAG configurations.

---

## 2. RAG Pipeline

```text
Documents
    |
    v
Document Loading
    |
    v
Chunking
    |
    v
Embedding Model
    |
    v
ChromaDB Vector Store
    |
    v
Query Embedding
    |
    v
Top-k Retrieval
    |
    v
Retrieved Context
    |
    v
Gemini LLM
    |
    v
Generated Answer
    |
    v
Evaluation Harness
