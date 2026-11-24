"""Export a 30-answer manual grading sheet (answers must be generated and graded separately)."""
import json,csv
from pathlib import Path
qs=[json.loads(x) for x in Path('data/eval/gold_questions.jsonl').read_text().splitlines() if x.strip() and json.loads(x)['in_scope']]
qs=qs[:30]
Path('evaluation/results').mkdir(parents=True,exist_ok=True)
with open('evaluation/results/manual_grading_template.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['question_id','question','reference_answer','generated_answer','correctness_0_1_2','citation_support_0_1','notes','grader'])
    for q in qs:w.writerow([q['id'],q['question'],q['reference_answer'],'','', '', '', ''])
print('Exported grading template for',len(qs),'questions.')
