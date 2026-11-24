from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / 'data' / 'raw'
PROCESSED_DIR = ROOT / 'data' / 'processed'
EVAL_DIR = ROOT / 'data' / 'eval'
RESULTS_DIR = ROOT / 'evaluation' / 'results'
CHUNKS_PATH = PROCESSED_DIR / 'chunks.jsonl'
INDEX_PATH = PROCESSED_DIR / 'index.joblib'
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai_compatible')
LLM_BASE_URL = os.getenv('LLM_BASE_URL', 'https://api.groq.com/openai/v1')
LLM_MODEL = os.getenv('LLM_MODEL', 'llama-3.1-8b-instant')
LLM_API_KEY = os.getenv('LLM_API_KEY', '')
DEFAULT_K = int(os.getenv('DEFAULT_K', '5'))
