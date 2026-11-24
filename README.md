# PolicyPilot 📘
### Evidence-Grounded Policy & Documentation QA with Hybrid Retrieval

PolicyPilot is a retrieval-based question-answering system designed to answer questions using retrieved documentation passages. It combines lexical retrieval (BM25), semantic retrieval (dense embeddings), and Reciprocal Rank Fusion (RRF) to improve document retrieval, provides source-aware responses, and includes evaluation tools for retrieval quality and out-of-scope question handling.

## Features

- **BM25 Retrieval:** Keyword-based retrieval for exact terminology.
- **Dense Retrieval:** Semantic search using Sentence Transformers.
- **Hybrid Retrieval:** Combines multiple retrieval rankings using Reciprocal Rank Fusion (RRF).
- **Evidence-Based QA:** Answers are based on retrieved passages.
- **Source Attribution:** Displays retrieved document sources.
- **Out-of-Scope Detection:** Evaluates the ability to identify questions outside the available corpus.
- **Retrieval Evaluation:** Recall@K and Mean Reciprocal Rank (MRR).
- **Interactive Interface:** Streamlit-based interface.

## Architecture

```text
User Query
    │
    ▼
Query Processing
    │
    ├──────────────► BM25 Retriever
    │
    └──────────────► Dense Retriever
                           │
                           ▼
                  Reciprocal Rank Fusion
                           │
                           ▼
                  Ranked Evidence Chunks
                           │
                           ▼
                    Answer Generation
                           │
                           ▼
                 Answer + Source Evidence
```

## Technology Stack

- Python
- Streamlit
- Sentence Transformers
- BM25
- Reciprocal Rank Fusion (RRF)
- JSONL-based document processing
- Pytest

## Dataset

The experimental corpus contains 45 selected Markdown documents from the public GitLab software documentation repository.

The documents were sampled from three documentation categories:

- Security
- Administration
- User documentation

The corpus was processed into **449 text chunks** using a chunk size of 320 tokens and an overlap of 40 tokens.

> This experimental corpus is a selected subset of GitLab software documentation and is not the GitLab Handbook.

## Retrieval Evaluation

PolicyPilot compares three retrieval strategies:

| Retriever | Description |
|---|---|
| BM25 | Lexical retrieval based on term relevance |
| Dense | Semantic retrieval using embedding similarity |
| Hybrid | Rank fusion of BM25 and dense retrieval |

### Test Results

| Method | Recall@1 | Recall@3 | Recall@5 | MRR |
|---|---:|---:|---:|---:|
| BM25 | 0.70 | 0.70 | 0.80 | 0.725 |
| Dense | 0.60 | 0.80 | 0.80 | 0.683 |
| Hybrid | **0.70** | **0.80** | **0.80** | **0.733** |

The hybrid retrieval approach achieved the highest MRR in this evaluation.

## Out-of-Scope Evaluation

A separate experiment evaluates the system's ability to distinguish in-scope and out-of-scope questions.

- Threshold selected using the development split.
- Evaluation performed on a held-out test split.
- Test balanced accuracy: **70.83%**
- Out-of-scope questions correctly refused: **5/5**
- In-scope questions incorrectly refused: **7/10**

These results indicate that the refusal threshold requires further tuning to reduce false refusals.

## Project Structure

```text
PolicyPilot/
├── policypilot/
│   ├── chunking.py
│   ├── config.py
│   ├── filter_corpus.py
│   ├── generate.py
│   ├── ingest.py
│   ├── qa.py
│   ├── refusal.py
│   └── retrievers.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── eval/
├── evaluation/
│   ├── eval_retrieval.py
│   ├── eval_refusal.py
│   ├── eval_chunks.py
│   └── results/
├── tests/
├── app.py
├── api.py
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd PolicyPilot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

## Build the Corpus

```bash
python -m policypilot.ingest --root data/raw/handbook_subset --max-tokens 320 --overlap 40
```

## Build Retrieval Index

```bash
python -c "from policypilot.retrievers import build_index; build_index(use_embeddings=True); print('Index built successfully')"
```

## Run Retrieval Evaluation

```bash
python evaluation/eval_retrieval.py
```

## Run Refusal Evaluation

```bash
python evaluation/eval_refusal.py
```

## Run Tests

```bash
pytest
```

## Limitations

- The evaluation dataset is relatively small and manually constructed.
- The documentation corpus is a selected subset rather than a comprehensive dataset.
- Retrieval relevance depends on corpus quality and query phrasing.
- Out-of-scope detection currently has a noticeable false-refusal rate.
- Answer synthesis requires a configured LLM provider; otherwise, the application can use an extractive fallback.

## Future Improvements

- Improve refusal calibration.
- Expand and diversify the evaluation dataset.
- Improve citation validation.
- Add more document sources.
- Evaluate chunking strategies systematically.
- Improve answer synthesis and evidence verification.
- Add user feedback and answer-quality evaluation.

## Disclaimer

PolicyPilot is an experimental documentation QA project. It is not a substitute for authoritative policy, security, legal, or compliance review.

---

**Built as an experiment in evidence-grounded question answering, hybrid information retrieval, and retrieval evaluation.**