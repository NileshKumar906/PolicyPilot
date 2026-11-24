
# PolicyPilot 📘

### Retrieval and Evaluation Prototype for Documentation Search

PolicyPilot is a retrieval and evaluation prototype designed to retrieve relevant documentation passages and display evidence with source links. It compares lexical retrieval (BM25), dense semantic retrieval using Sentence Transformers, and hybrid retrieval using Reciprocal Rank Fusion (RRF).

The prototype focuses on retrieval quality, evidence presentation, source attribution, and preliminary evaluation of retrieval-based refusal behavior.

> **Current status:** PolicyPilot retrieves and displays relevant documentation passages with source links. LLM-based answer synthesis is not currently configured.

---

## Features

- **BM25 Retrieval:** Lexical search based on term relevance.
- **Dense Retrieval:** Semantic retrieval using `all-MiniLM-L6-v2`.
- **Hybrid Retrieval:** Combines retrieval rankings using Reciprocal Rank Fusion (RRF).
- **Evidence Display:** Presents retrieved passages with source attribution.
- **Source Links:** Displays links to the original documentation.
- **Refusal Gate:** Experimental retrieval-score threshold used to decide whether retrieved evidence is sufficient.
- **Evaluation Framework:** Scripts to evaluate retrieval performance and refusal behavior.
- **Streamlit Interface:** Interactive interface for testing retrieval.
- **FastAPI:** API interface for querying the retrieval pipeline.
- **Automated Tests:** Tests covering API behavior, chunking, and ranking fusion.

---

## Architecture

```text
                    User Query
                        |
                Query Processing
                        |
             +----------+----------+
             |                     |
          BM25 Search         Dense Search
             |                     |
             +----------+----------+
                        |
                  Hybrid RRF
                        |
                Ranked Evidence
                        |
                 Refusal Gate
                        |
             Evidence Display /
              Extractive Fallback
                        |
                  Source Links
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| API | FastAPI |
| Lexical Retrieval | BM25 |
| Dense Retrieval | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Hybrid Retrieval | Reciprocal Rank Fusion |
| Testing | pytest |

---

## Dataset

The prototype uses a selected subset of GitLab documentation for retrieval experimentation.

- **Documents selected:** 45
- **Categories:** Security, Administration, User documentation
- **Chunks generated:** 449
- **Chunk size:** 320 tokens
- **Overlap:** 40 tokens

The selected corpus is a small experimental subset, not a comprehensive documentation collection.

The source is GitLab product documentation, not the GitLab Handbook.

See [DATA_ATTRIBUTION.md](docs/DATA_ATTRIBUTION.md) for source and attribution details.

---

## Retrieval Evaluation

The retrieval evaluation compares BM25, Dense, and Hybrid retrieval on a manually constructed evaluation dataset.

The in-scope retrieval test split contains **10 questions**.

### Test Results

| Retriever | Recall@1 | Recall@3 | Recall@5 | MRR |
|---|---:|---:|---:|---:|
| BM25 | 0.70 | 0.70 | 0.80 | 0.725 |
| Dense | 0.60 | 0.80 | 0.80 | 0.683 |
| Hybrid (RRF) | 0.70 | 0.80 | 0.80 | 0.733 |

All three retrievers achieved Recall@5 of 0.80 on the 10-question in-scope test split.

Hybrid had the highest observed MRR (0.733), but the evaluation is small and does not establish that any retriever is superior.

### Interpretation

- All three retrievers retrieved a relevant document within the top five results for 8 of the 10 in-scope test questions.
- MRR measures how highly the first relevant result is ranked.
- The results are preliminary and should not be generalized beyond this small dataset.

---

## Refusal Gate Evaluation

The prototype includes an experimental retrieval-score threshold that can refuse queries when retrieval scores fall below a configured threshold.

The threshold was selected using the development split and evaluated on a held-out test split containing 15 questions:

- 10 in-scope questions
- 5 out-of-scope questions

### Test Results

| Metric | Result |
|---|---:|
| In-scope questions | 10 |
| Out-of-scope questions | 5 |
| False refusals | 7/10 (70%) |
| Correct out-of-scope refusals | 5/5 |
| Overall accuracy | 8/15 (53.33%) |
| Balanced accuracy | 65% |

### Interpretation

The refusal gate over-refuses in-scope questions, with a false-refusal rate of 70%.

Although all 5 out-of-scope test questions were refused, this is not evidence of good discrimination because the gate also falsely refuses a substantial proportion of valid in-scope questions.

The refusal mechanism therefore remains experimental and requires further calibration and evaluation.

---

## Project Structure

```text
PolicyPilot/
│
├── api.py
├── app.py
├── create_eval_questions.py
├── fetch_handbook.py
├── requirements.txt
├── README.md
│
├── policypilot/
│   ├── chunking.py
│   ├── config.py
│   ├── filter_corpus.py
│   ├── generate.py
│   ├── ingest.py
│   ├── qa.py
│   ├── refusal.py
│   └── retrievers.py
│
├── data/
│   ├── eval/
│   ├── raw/
│   │   └── demo_corpus/
│   └── processed/
│
├── docs/
│   ├── DATA_ATTRIBUTION.md
│   ├── EXPERIMENT_PROTOCOL.md
│   └── architecture.svg
│
├── evaluation/
│   ├── eval_chunks.py
│   ├── eval_refusal.py
│   ├── eval_retrieval.py
│   ├── export_grading.py
│   └── results/
│
└── tests/
    ├── test_api.py
    ├── test_chunking.py
    └── test_rrf.py
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/NileshKumar906/PolicyPilot.git
cd PolicyPilot
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```powershell
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Quickstart: Demo Corpus

The repository includes a small demo corpus for reproducible local testing.

### 1. Build the Corpus

```bash
python -m policypilot.ingest --root data/raw/demo_corpus --max-tokens 320 --overlap 40
```

### 2. Build the Retrieval Index

```bash
python -c "from policypilot.retrievers import build_index; build_index(use_embeddings=True); print('Index built successfully')"
```

### 3. Launch the Streamlit App

```bash
streamlit run app.py
```

---

## Run the API

Start the API server:

```bash
uvicorn api:app --reload
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

---

## Run Tests

```bash
pytest
```

The project's current automated test suite contains 5 tests covering API behavior, chunking, and RRF.

---

## Evaluation Scripts

Run retrieval evaluation:

```bash
python evaluation/eval_retrieval.py
```

Run refusal threshold evaluation:

```bash
python evaluation/eval_refusal.py
```

Evaluation outputs are stored in:

```text
evaluation/results/
```

---

## Limitations

- Small, manually constructed evaluation dataset.
- Single documentation corpus and selected subset.
- Evaluation questions are manually designed.
- Results are preliminary and do not establish retriever superiority.
- LLM-based synthesis is not currently configured.
- The refusal gate has a 70% false-refusal rate on the test split.
- The corpus is GitLab product documentation, not the GitLab Handbook.
- The experiment does not represent a production documentation search system.

---

## Future Improvements

- Expand the evaluation dataset.
- Evaluate on additional documentation corpora.
- Improve refusal calibration.
- Add a reranker.
- Implement grounded LLM synthesis.
- Add automated citation validation.
- Improve retrieval relevance and ranking evaluation.

---

## License

This repository's code is released under the MIT License.

See [LICENSE](LICENSE) for details.

Dataset and source-document attribution are addressed separately in [DATA_ATTRIBUTION.md](docs/DATA_ATTRIBUTION.md).

---

## Disclaimer

PolicyPilot is an experimental retrieval and evaluation prototype developed for learning and research purposes. Evaluation results are based on a small manually constructed dataset and should not be interpreted as evidence of production-level reliability.
