# PolicyPilot experiment protocol

## Dataset status
The bundled starter dataset is a small **fictional demo corpus**, not the GitLab Handbook. Its 75-question set is a scaffold: 60 in-scope and 15 out-of-scope, with dev/test labels. It is useful for smoke tests and exercising the evaluation scripts, not for portfolio claims about the GitLab corpus.

## GitLab corpus
1. Review GitLab's handbook repository license and attribution requirements.
2. Run `python fetch_handbook.py` and `python policypilot/filter_corpus.py`.
3. Review the selected paths. The selection script is heuristic, not a validated corpus curation process.
4. Ingest the selected subset with `python -m policypilot.ingest --root data/raw/handbook_subset`.
5. Record the retrieval date, commit hash, corpus page count and license in the report.

## Questions and split
Starter questions are hand-authored, paraphrased to some degree, but are not yet independently validated against GitLab pages. Dev/test split is fixed in the JSONL file. For a real evaluation, verify gold pages and reference answers, avoid duplicates, and lock the test set before experiments.

## Metrics
Retrieval script reports Recall@1/3/5 and MRR for in-scope questions. It compares BM25, embeddings and RRF hybrid. `eval_refusal.py` selects a threshold using dev questions and reports test results separately. The refusal score is retriever-specific and this threshold approach is intentionally simple.

## Answer grading
`evaluation/results/manual_grading_template.csv` is a blank sheet. Do not claim answer correctness or citation-support rates until answers have been generated, graded by a human, and the sheet has been completed. Suggested rubric: correctness 0=wrong, 1=partially correct, 2=correct; citation support 0=unsupported/missing, 1=directly supported.

## Chunk ablation
`eval_chunks.py` compares approximate chunk sizes with BM25 test Recall@5 and restores the original artifacts after the run. Treat the test-set ablation as exploratory unless a single experiment plan was pre-registered/locked; do not use repeated test tuning to select a final configuration.

## Initial BM25 smoke result on bundled demo corpus
A quick full-set BM25 smoke run on the 60 in-scope starter questions returned Recall@1 0.75, Recall@3 0.9167, Recall@5 0.9667 and MRR 0.8303. These figures are for the small fictional demo corpus and full starter-question set, not a held-out benchmark, not GitLab data, and not a final resume result. They should not be used as evidence of generalized performance.
