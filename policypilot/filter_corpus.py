"""Copy a relevant handbook subset from cloned GitLab repo to the indexed raw directory."""
from pathlib import Path
import shutil
SRC=Path('data/raw/gitlab-handbook/doc'); OUT=Path('data/raw/handbook_subset')
KEYWORDS=('people','security','enterprise','technology','remote','onboarding','expense','leave','access','device','support','password','incident','benefit')
MAX_FILES=180
if not SRC.exists(): raise SystemExit('Run python fetch_handbook.py first.')
selected=[]
for p in SRC.rglob('*.md'):
    rel=p.relative_to(SRC).as_posix().lower()
    if any(k in rel for k in KEYWORDS): selected.append(p)
selected=sorted(selected)[:MAX_FILES]
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)
for p in selected:
    dest=OUT/p.relative_to(SRC); dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dest)
print(f'Copied {len(selected)} Markdown files to {OUT}. Review paths for relevance before treating this as a curated corpus.')
