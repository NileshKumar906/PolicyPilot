"""Evaluate retrieval Recall@k and MRR using gold page references; untouched test metrics are reported separately."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]) )
from policypilot.retrievers import build_index,search
from policypilot.config import EVAL_DIR,RESULTS_DIR

def match_gold(doc,gold):
    path=doc.get('source_path','').lower(); title=doc.get('page_title','').lower()
    return any(g.lower() in path or g.lower() in title for g in gold)
def main():
    qs=[json.loads(x) for x in (EVAL_DIR/'gold_questions.jsonl').read_text().splitlines() if x.strip()]
    chunks_path=Path('data/processed/chunks.jsonl')
    if not chunks_path.exists(): raise SystemExit('Run ingestion first.')
    index=build_index(use_embeddings=True)
    RESULTS_DIR.mkdir(parents=True,exist_ok=True); summary=[]; per=[]
    for strategy in ('bm25','embedding','hybrid'):
        for split in ('dev','test'):
            subset=[q for q in qs if q['split']==split and q['in_scope']]
            rows=[]
            for q in subset:
                results=search(q['question'],strategy,5,index)
                ranks=[i for i,d in enumerate(results,1) if match_gold(d,q['gold_pages'])]
                rank=min(ranks) if ranks else None
                rows.append({'question_id':q['id'],'strategy':strategy,'split':split,'gold_rank':rank,'recall_at_1':bool(rank and rank<=1),'recall_at_3':bool(rank and rank<=3),'recall_at_5':bool(rank and rank<=5),'reciprocal_rank':1/rank if rank else 0})
            if rows:
                summary.append({'strategy':strategy,'split':split,'n':len(rows),'recall@1':sum(r['recall_at_1'] for r in rows)/len(rows),'recall@3':sum(r['recall_at_3'] for r in rows)/len(rows),'recall@5':sum(r['recall_at_5'] for r in rows)/len(rows),'mrr':sum(r['reciprocal_rank'] for r in rows)/len(rows)})
                per.extend(rows)
    (RESULTS_DIR/'retrieval_metrics.json').write_text(json.dumps(summary,indent=2))
    import csv
    for name,rows in [('retrieval_metrics.csv',summary),('per_question_retrieval.csv',per)]:
        with (RESULTS_DIR/name).open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
