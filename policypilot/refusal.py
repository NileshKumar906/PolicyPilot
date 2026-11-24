"""Retriever-score refusal gate. Thresholds are configuration, not universal truth."""
import os

def should_refuse(results, retriever='hybrid', threshold=None):
    if not results: return True, 0.0
    if threshold is None:
        threshold=float(os.getenv('REFUSAL_THRESHOLD', '0.012' if retriever=='hybrid' else '0.20' if retriever=='embedding' else '2.0'))
    score=float(results[0].get('score',0))
    return score < threshold, score
