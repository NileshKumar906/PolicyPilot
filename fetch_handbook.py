"""Fetch the public GitLab handbook repository (shallow clone) for local subset filtering.
Requires git and internet access. Clone is intentionally separate from the app runtime.
"""
import subprocess, sys
from pathlib import Path
DEST=Path('data/raw/gitlab-handbook')
if DEST.exists():
    print(f'{DEST} already exists; remove it to re-clone.'); sys.exit(0)
DEST.parent.mkdir(parents=True,exist_ok=True)
cmd=['git','clone','--depth','1','https://gitlab.com/gitlab-org/gitlab.git',str(DEST)]
print('Cloning repository. This may take a while...')
try: subprocess.run(cmd,check=True)
except Exception as e: print('Clone failed:',e); sys.exit(1)
print('Clone complete. Markdown documents under doc/ will be available to ingestion.')
