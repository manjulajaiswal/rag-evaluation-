# RAG Evaluation Benchmark

A small, end-to-end Retrieval-Augmented Generation (RAG) evaluation system built to measure not only whether the correct documents are retrieved, but also whether the retrieved context actually supports the answer and whether the generated answer is correct and grounded.

The project includes a parameterized RAG pipeline, an evaluation harness, controlled experiments across chunking / top-k / embedding configurations, checkpointing for API resilience, and an interactive Google Apps Script dashboard.

---

## 1. Project Overview

The system evaluates a RAG pipeline across three levels:

1. **Document-level retrieval**
   - Did retrieval find the correct source documents?

2. **Context-level retrieval**
   - Did the retrieved chunks actually contain the information needed to answer the question?
   - Were relevant chunks ranked above irrelevant ones?

3. **Generation quality**
   - Was the final answer faithful to the retrieved context?
   - Did it match the expected answer?

This separation makes it possible to distinguish:

> Retrieval failure → Context failure → Generation failure

instead of relying on a single end-to-end score.

---

## 2. Dataset

The benchmark uses a small domain-specific corpus focused on **computer vision for badminton analysis**.

### Documents

The dataset contains **17 short documents** covering topics such as:

- badminton computer vision overview
- shuttlecock detection
- shuttlecock tracking
- TrackNet
- TrackNetV3
- player detection
- player tracking
- pose estimation
- hit detection
- rally analysis
- court analysis
- trajectory analysis
- badminton datasets
- video analysis pipeline
- shot classification
- performance analytics
- YOLO

The documents are intentionally concise so that retrieval behavior can be inspected and evaluated easily.

### Evaluation Questions

The benchmark contains **16 questions** covering different reasoning patterns:

- single-hop questions
- paraphrasing
- comparative questions
- multi-hop questions
- conditional questions
- abstract questions
- counterfactual questions

A ground-truth file stores:

- question ID
- question
- expected answer
- relevant source document(s)

---

## 3. RAG Pipeline

The pipeline is:

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Query embedding
    ↓
Top-k retrieval
    ↓
Retrieved context
    ↓
Gemini generation
    ↓
Answer
