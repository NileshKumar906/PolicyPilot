"""Chunk-size ablation: rebuild chunk files/index temporarily for 200 vs 320-word-ish token targets."""
import json,sys,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]) )
from policypilot.ingest import build_chunks
from policypilot.retrievers import build_index,search
from policypilot.config import CHUNKS_PATH,INDEX_PATH,RESULTS_DIR

def score(questions,index):
    def match_gold(doc,gold):
        path=doc.get('source_path','').lower(); title=doc.get('page_title','').lower()
        return any(g.lower() in path or g.lower() in title for g in gold)
    subset=[q for q in questions if q['split']=='test' and q['in_scope']]
    rows=[]
    for q in subset:
        result=search(q['question'],'bm25',5,index); ranks=[i for i,d in enumerate(result,1) if match_gold(d,q['gold_pages'])]
        rows.append(bool(ranks and ranks[0]<=5))
    return sum(rows)/len(rows) if rows else 0

def main():
    questions=[json.loads(x) for x in Path('data/eval/gold_questions.jsonl').read_text().splitlines()]
    RESULTS_DIR.mkdir(parents=True,exist_ok=True); records=[]
    old_chunks=CHUNKS_PATH.read_bytes() if CHUNKS_PATH.exists() else None
    old_index=INDEX_PATH.read_bytes() if INDEX_PATH.exists() else None
    for size in (220,320,420):
        chunks=build_chunks(max_tokens=size,overlap=40); index=build_index(chunks,use_embeddings=False)
        records.append({'chunk_token_target':size,'test_recall_at_5_bm25':score(questions,index),'chunk_count':len(chunks)})
    (RESULTS_DIR/'chunk_ablation.json').write_text(json.dumps(records,indent=2)); print(json.dumps(records,indent=2))
    # Restore default artifacts after this exploratory ablation.
    if old_chunks is not None: CHUNKS_PATH.write_bytes(old_chunks)
    if old_index is not None: INDEX_PATH.write_bytes(old_index)
if __name__=='__main__':main()
