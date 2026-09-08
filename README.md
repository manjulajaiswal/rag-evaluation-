# RAG Evaluation Benchmark

An end-to-end Retrieval-Augmented Generation (RAG) evaluation pipeline built on a small badminton computer-vision dataset.

The project evaluates RAG at three levels:

- **Document retrieval** — did we retrieve the right sources?
- **Context quality** — did the retrieved chunks contain the needed evidence?
- **Answer quality** — was the answer correct and grounded?

**Live Dashboard:**  
https://script.google.com/macros/s/AKfycbyXke3F-lLe9He_y5ah98b9vNS6_kZV291UAD1DBKcFZOx_20A9tgQUuyv8iHUallZ-Lg/exec

---

## Dataset

- **17 documents**
- **16 evaluation questions**
- Topics include shuttle tracking, TrackNet/TrackNetV3, YOLO, player detection, pose estimation, rally analysis, shot classification, and performance analytics.
- Questions cover single-hop, paraphrasing, comparative, multi-hop, conditional, abstract, and counterfactual cases.

---

## RAG Pipeline

```text
Documents
   ↓
Chunking
   ↓
Embeddings
   ↓
ChromaDB
   ↓
Top-k Retrieval
   ↓
Gemini Generation
```

The pipeline is configurable for chunk size, top-k, and embedding model.

---

## Evaluation Metrics

### Retrieval

- **Document Precision**
- **Document Recall**
- **Context Precision**
- **Context Recall**

### Generation

- **Faithfulness**
- **Correctness**

### Composite

A project-defined RAGAS-style composite:

```text
(Context Precision + Context Recall + Faithfulness + Correctness) / 4
```

This is a project-defined score, not an official Ragas score.

---

## Experiments

Seven configurations were evaluated:

| Configuration | Chunk | Top-k | Embedding |
|---|---:|---:|---|
| chunk_small | 80 | 3 | MiniLM |
| chunk_large | 160 | 3 | MiniLM |
| topk_2 | 80 | 2 | MiniLM |
| topk_5 | 80 | 5 | MiniLM |
| embed_minilm | 80 | 3 | MiniLM |
| embed_mpnet | 80 | 3 | MPNet |
| final_combined | 160 | 5 | MiniLM |

Controlled experiments isolate:

- chunk size
- top-k
- embedding model

---

## Results

| Configuration | Doc P | Doc R | Context P | Context R | Faithfulness | Correctness | Composite |
|---|---:|---:|---:|---:|---:|---:|---:|
| chunk_small | 0.604 | 0.661 | 0.745 | 0.812 | 1.000 | 0.750 | 0.827 |
| chunk_large | 0.604 | 0.766 | 0.760 | 0.938 | 1.000 | 0.938 | 0.909 |
| topk_2 | 0.688 | 0.661 | 0.781 | 0.755 | 1.000 | 0.812 | 0.837 |
| topk_5 | 0.562 | 0.870 | 0.730 | 0.880 | 1.000 | 0.875 | 0.871 |
| embed_minilm | 0.604 | 0.661 | 0.938 | 0.833 | 1.000 | 0.812 | 0.896 |
| embed_mpnet | 0.583 | 0.672 | 0.885 | 0.833 | 1.000 | 0.812 | 0.883 |
| **final_combined** | **0.463** | **0.870** | **0.762** | **1.000** | **1.000** | **1.000** | **0.940** |

### Main findings

- Increasing chunk size from **80 → 160** improved context recall and correctness.
- Increasing top-k from **2 → 5** improved recall, but reduced precision.
- MPNet slightly improved document recall but reduced overall composite.
- The final configuration achieved the best overall benchmark result.

### Final configuration

```text
Chunk size : 160
Overlap    : 20
Top-k      : 5
Embedding  : all-MiniLM-L6-v2
Composite  : 0.940
```

A key trade-off is lower document precision (`0.463`) in exchange for high document recall (`0.870`) and full context recall (`1.000`).

---

## Failure Analysis

The benchmark includes examples of:

- semantic retrieval misses
- missing multi-hop evidence
- downstream dependency misses
- cases where context was available but the generated answer was still incorrect

This helps separate retrieval problems from generation problems.

---

## Reliability

The evaluation harness includes:

- retry logic with exponential backoff
- checkpointing
- resume support

This avoids restarting long LLM evaluation runs after transient API failures.

---

## Project Structure

```text
rag-evaluation/
├── configs/
├── data/
├── results/
├── src/
├── dashboard/
├── compare.py
├── run_config.py
├── inspect_results.py
├── requirements.txt
└── README.md
```

---

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the API key:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Run an evaluation:

```bash
python src/evaluation.py --config configs/chunk_small.json
```

Compare completed runs:

```bash
python compare.py
```

`compare.py` reads the existing result files and does not rerun the LLM evaluations.

---

## Limitations

- Small benchmark: 17 documents and 16 questions.
- LLM-based evaluation can have evaluator variance.
- Document-level metrics are coarser than chunk-level context metrics.
- Faithfulness is 1.000 across all seven runs, so it does not distinguish configurations here.
- Current retrieval is vector-only; no BM25, hybrid retrieval, or reranking.

## Future Improvements

- Hybrid BM25 + vector retrieval
- Cross-encoder reranking
- Larger evaluation sets
- Latency and token-cost tracking
- CI regression gates
