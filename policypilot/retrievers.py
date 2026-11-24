"""BM25, local embedding cosine retrieval, and reciprocal-rank hybrid retrieval."""
import re, json, joblib
import numpy as np
from pathlib import Path
try:
    from rank_bm25 import BM25Okapi
except ImportError:
    class BM25Okapi:
        """Small dependency-free BM25 implementation (Okapi variant)."""
        def __init__(self, corpus, k1=1.5, b=0.75):
            from collections import Counter
            self.corpus=corpus; self.k1=k1; self.b=b; self.n=len(corpus)
            self.tf=[Counter(doc) for doc in corpus]; self.dl=[len(doc) for doc in corpus]
            self.avgdl=sum(self.dl)/max(1,self.n); df=Counter()
            for doc in corpus: df.update(set(doc))
            self.idf={w:np.log(1+(self.n-df[w]+0.5)/(df[w]+0.5)) for w in df}
        def get_scores(self, query):
            scores=np.zeros(self.n)
            for term in query:
                idf=self.idf.get(term,0)
                for i,tf in enumerate(self.tf):
                    f=tf.get(term,0); dl=self.dl[i]
                    if f: scores[i]+=idf*f*(self.k1+1)/(f+self.k1*(1-self.b+self.b*dl/max(1,self.avgdl)))
            return scores
from .config import CHUNKS_PATH, INDEX_PATH, EMBEDDING_MODEL, PROCESSED_DIR

def tokenize(text): return re.findall(r"[a-z0-9_]+", text.lower())

def load_chunks(path=CHUNKS_PATH):
    if not Path(path).exists(): raise FileNotFoundError(f'Chunk file not found: {path}. Run python -m policypilot.ingest first.')
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]

def build_index(chunks=None, use_embeddings=True):
    chunks=chunks or load_chunks(); corpus=[tokenize(c['text']) for c in chunks]
    bm25=BM25Okapi(corpus)
    embeddings=None; model_name=None
    if use_embeddings:
        try:
            from sentence_transformers import SentenceTransformer
            model=SentenceTransformer(EMBEDDING_MODEL)
            embeddings=model.encode([c['text'] for c in chunks],normalize_embeddings=True,show_progress_bar=True)
            model_name=EMBEDDING_MODEL
        except Exception as exc:
            print(f'Embedding model unavailable; building BM25-only index: {exc}')
    data={'chunks':chunks,'bm25':bm25,'tokens':corpus,'embeddings':embeddings,'embedding_model':model_name}
    PROCESSED_DIR.mkdir(parents=True,exist_ok=True); joblib.dump(data,INDEX_PATH)
    return data

def load_index():
    if not INDEX_PATH.exists(): return build_index()
    return joblib.load(INDEX_PATH)

def bm25_search(query,k=5,index=None):
    index=index or load_index(); scores=index['bm25'].get_scores(tokenize(query))
    order=np.argsort(scores)[::-1][:k]
    return [{**index['chunks'][i], 'score':float(scores[i]),'retriever':'bm25'} for i in order]

def embedding_search(query,k=5,index=None):
    index=index or load_index()
    if index.get('embeddings') is None: raise RuntimeError('Embedding index unavailable. Rebuild with sentence-transformers installed and network/model access.')
    from sentence_transformers import SentenceTransformer
    model=SentenceTransformer(index['embedding_model'] or EMBEDDING_MODEL)
    q=model.encode([query],normalize_embeddings=True)[0]
    scores=np.asarray(index['embeddings']) @ q
    order=np.argsort(scores)[::-1][:k]
    return [{**index['chunks'][i],'score':float(scores[i]),'retriever':'embedding'} for i in order]

def rrf(results_lists,k=5,constant=60):
    scores={}; docs={}
    for result_list in results_lists:
        for rank,doc in enumerate(result_list,1):
            key=doc['chunk_id']; scores[key]=scores.get(key,0)+1/(constant+rank); docs[key]=doc
    ranked=sorted(scores,key=scores.get,reverse=True)[:k]
    return [{**docs[key],'score':scores[key],'retriever':'hybrid'} for key in ranked]

def search(query,retriever='hybrid',k=5,index=None):
    index=index or load_index()
    if retriever=='bm25': return bm25_search(query,k,index)
    if retriever in ('embedding','embeddings'): return embedding_search(query,k,index)
    if retriever=='hybrid':
        lexical=bm25_search(query,max(k,10),index)
        try: semantic=embedding_search(query,max(k,10),index)
        except Exception as exc:
            print(f'Hybrid degraded to BM25 because embeddings are unavailable: {exc}')
            return [{**d,'retriever':'hybrid'} for d in lexical[:k]]
        return rrf([lexical,semantic],k)
    raise ValueError(f'Unknown retriever: {retriever}')
