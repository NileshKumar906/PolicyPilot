"""Tune refusal threshold on dev only, then evaluate the chosen threshold on test.
Scores are retriever-specific; this simple study uses hybrid RRF scores.
"""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from policypilot.retrievers import build_index,search
from policypilot.config import RESULTS_DIR

def main():
    qs=[json.loads(x) for x in Path('data/eval/gold_questions.jsonl').read_text().splitlines()]
    index=build_index(use_embeddings=True); cache={}
    for q in qs:
        r=search(q['question'],'hybrid',5,index); cache[q['id']]=float(r[0]['score']) if r else 0
    dev=[q for q in qs if q['split']=='dev']; test=[q for q in qs if q['split']=='test']
    thresholds=sorted(set([0.0]+[cache[q['id']] for q in dev]+[max(cache.values())+1]))
    best=None
    for t in thresholds:
        tp=sum(not q['in_scope'] and cache[q['id']]<t for q in dev); tn=sum(q['in_scope'] and cache[q['id']]>=t for q in dev)
        fp=sum(not q['in_scope'] and cache[q['id']]>=t for q in dev); fn=sum(q['in_scope'] and cache[q['id']]<t for q in dev)
        acc=(tp+tn)/len(dev); balanced=((tp/(tp+fn) if tp+fn else 0)+(tn/(tn+fp) if tn+fp else 0))/2
        candidate={'threshold':t,'dev_accuracy':acc,'dev_balanced_accuracy':balanced,'dev_true_refusals':tp,'dev_false_refusals':fn,'dev_missed_out_of_scope':fp}
        if best is None or balanced>best['dev_balanced_accuracy']:best=candidate
    t=best['threshold']; tp=sum(not q['in_scope'] and cache[q['id']]<t for q in test); tn=sum(q['in_scope'] and cache[q['id']]>=t for q in test); fp=sum(not q['in_scope'] and cache[q['id']]>=t for q in test); fn=sum(q['in_scope'] and cache[q['id']]<t for q in test)
    best.update({'test_n':len(test),'test_true_refusals':tp,'test_false_refusals':fn,'test_missed_out_of_scope':fp,'test_balanced_accuracy':((tp/(tp+fn) if tp+fn else 0)+(tn/(tn+fp) if tn+fp else 0))/2,'warning':'Threshold chosen on dev; test metrics are held out. Starter demo corpus and hand-written questions only.'})
    RESULTS_DIR.mkdir(parents=True,exist_ok=True); (RESULTS_DIR/'refusal_threshold.json').write_text(json.dumps(best,indent=2)); print(json.dumps(best,indent=2))
if __name__=='__main__':main()
