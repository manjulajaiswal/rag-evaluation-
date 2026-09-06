# RAG Evaluation Harness

A small Retrieval-Augmented Generation (RAG) system with an evaluation
harness for measuring retrieval quality, answer faithfulness, and answer
correctness across different pipeline configurations.

The main goal of the project is not only to generate answers, but to
determine whether a change to the RAG pipeline actually improves or
regresses its performance.

## Evaluation Dashboard

Interactive dashboard showing the evaluation results for Config A vs Config B.

[Open RAG Evaluation Dashboard](https://script.google.com/macros/s/AKfycbzVBVcmop2OgMq2J7iVlE8yK-4cf0YvuDqWkywEvUaqZ2yBB7EvLWR19clQfYslt5nh/exec)

---

## 1. Project Overview

The system implements a complete RAG pipeline:

Documents → Chunking → Embeddings → ChromaDB → Retrieval → LLM → Answer

The evaluation harness then measures:

- Retrieval Precision
- Retrieval Recall
- Answer Faithfulness
- Answer Correctness

Two different chunking configurations are evaluated using the same:

- Document dataset
- Evaluation questions
- Embedding model
- Top-k value
- Generation model
- Evaluation methodology

This allows the experiment to isolate the effect of chunk size and overlap.

---

## 2. Dataset

The project uses a custom synthetic dataset containing 10 short
technology-company documents.

Each document contains information about a fictional company, including
products, technologies, dates, and use cases.

The evaluation set contains 10 questions. Each question includes:

- Question
- Expected answer
- Relevant source document

The relevant source document provides the ground truth used for evaluating
retrieval.

---

## 3. RAG Pipeline

### Step 1: Document Loading

Text documents are loaded from:

`data/documents/`

Each document is represented using:

- `document_id`
- `text`

### Step 2: Chunking

Documents are divided into smaller word-based chunks.

Two configurations are evaluated:

| Configuration | Chunk Size | Overlap |
|---|---:|---:|
| Config A | 80 words | 20 words |
| Config B | 160 words | 40 words |

Chunk size is the primary variable being compared.

The overlap helps reduce information loss at chunk boundaries.

### Step 3: Embeddings

The project uses:

`sentence-transformers/all-MiniLM-L6-v2`

Each chunk is converted into a 384-dimensional embedding vector.

The same embedding model is used for both configurations.

### Step 4: Vector Store

Embeddings and chunk metadata are stored in ChromaDB.

Each chunk stores metadata identifying its source document.

### Step 5: Retrieval

For every question:

1. The question is embedded using the same embedding model.
2. ChromaDB performs similarity search.
3. The top 3 chunks are retrieved.

`top_k = 3` is fixed across both configurations.

### Step 6: Generation

The retrieved chunks are passed to Gemini along with the question.

The generation prompt instructs the model to answer using only the
provided context and to explicitly state when the context does not contain
enough information.

---

## 4. Evaluation Harness

The evaluation harness evaluates every question independently.

### Retrieval Precision

Precision measures how much of the retrieved material was relevant.

Precision = Relevant Retrieved / Total Retrieved

For this project, relevance is evaluated at the source-document level.

For example, if the relevant source is `company_09.txt` and the top 3
retrieved chunks come from:

- `company_09.txt`
- `company_09.txt`
- `company_01.txt`

then:

Precision = 2 / 3 = 66.67%

### Retrieval Recall

Recall measures whether the relevant source was retrieved.

Recall = Relevant Retrieved / Total Relevant

Because each evaluation question has one known relevant source document,
recall is:

- 1 if the relevant source appears in the retrieved results
- 0 otherwise

### Answer Faithfulness

Faithfulness checks whether factual claims in the generated answer are
supported by the retrieved context.

An LLM judge evaluates whether the generated answer contains unsupported
claims or hallucinations.

### Answer Correctness

Correctness checks whether the generated answer agrees with the expected
answer and avoids materially incorrect factual claims.

An LLM judge is used for this evaluation.

---

## 5. Regression Experiment

The core experiment compares two chunking configurations.

All other pipeline variables remain fixed.

| Variable | Config A | Config B |
|---|---|---|
| Chunk size | 80 | 160 |
| Chunk overlap | 20 | 40 |
| Top-k | 3 | 3 |
| Embedding model | all-MiniLM-L6-v2 | all-MiniLM-L6-v2 |
| Generation model | Gemini | Gemini |
| Evaluation questions | Same 10 | Same 10 |

The hypothesis was that smaller chunks may provide more focused retrieval,
while larger chunks may preserve more surrounding context.

The experiment does not assume that either configuration will perform
better before evaluation.

---

## 6. Results

### Aggregate Results

| Metric | Config A | Config B | Winner |
|---|---:|---:|---|
| Retrieval Precision | **96.67%** | 63.33% | **Config A** |
| Retrieval Recall | 100.00% | 100.00% | Tie |
| Faithfulness | 100.00% | 100.00% | Tie |
| Correctness | 100.00% | 100.00% | Tie |

### Interpretation

Config A produced substantially better retrieval precision.

Both configurations achieved 100% retrieval recall, meaning the relevant
source was retrieved for every evaluation question.

However, Config B frequently included an additional irrelevant source in
the top-3 results. This reduced precision from 96.67% to 63.33%.

Despite the lower retrieval precision, the relevant information was still
available to the generator, so both configurations achieved 100%
faithfulness and correctness on this evaluation set.

### Per-Question Pattern

Config A:

- q01: 66.67% precision
- q02-q10: 100% precision

Config B:

- q01: 33.33% precision
- q02-q10: 66.67% precision

Both configurations achieved 100% recall on every question.

---

## 7. Key Tradeoff

The experiment demonstrates a chunking tradeoff.

### Smaller chunks

Advantages:

- More focused retrieval units
- Less irrelevant information per retrieved chunk
- Higher retrieval precision in this experiment

Potential disadvantage:

- Very small chunks can lose surrounding context and may hurt recall on
  documents where information is spread across boundaries.

### Larger chunks

Advantages:

- More surrounding context
- Better chance that related information appears within the same chunk

Potential disadvantages:

- More unrelated information can be retrieved together
- Lower retrieval precision in this experiment
- More irrelevant context may be passed to the generator

Therefore, the result should not be interpreted as "smaller chunks are
always better."

For this dataset, the 80/20 configuration was the better choice because it
improved retrieval precision without sacrificing recall or downstream
answer quality.

---

## 8. Failure Diagnosis

RAG retrieval and generation are evaluated separately.

When an answer is wrong, the first step is to inspect the retrieved chunks.

### Retrieval failure

If the retrieved context does not contain the information required to
answer the question, the problem is primarily a retrieval failure.

Possible causes include:

- Poor chunk size
- Poor chunk boundaries
- Embedding mismatch
- Insufficient top-k
- Semantic similarity failure

### Generation failure

If the retrieved context contains the required information but the model
still produces an incorrect or unsupported answer, the problem is more
likely in the generation stage.

Possible causes include:

- Prompt design
- Context interpretation
- Model behavior
- Unsupported inference by the LLM

This separation makes the evaluation harness useful for debugging rather
than only producing a single overall score.

---

## 9. Project Structure

```text
rag-evaluation/
│
├── data/
│   ├── documents/
│   │   ├── company_01.txt
│   │   ├── ...
│   │   └── company_10.txt
│   │
│   └── eval_questions.json
│
├── src/
│   ├── __init__.py
│   ├── chunker.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── index_documents.py
│   ├── retriever.py
│   ├── generator.py
│   ├── rag_pipeline.py
│   ├── evaluation.py
│   │
│   └── evaluators/
│       ├── retrieval.py
│       └── llm_judge.py
│
├── configs/
│
├── results/
│   ├── config_a_results.json
│   └── config_b_results.json
│
├── compare.py
├── README.md
└── requirements.txt
