from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from policypilot.qa import ask

app=FastAPI(title='PolicyPilot API',version='0.1.0',description='Grounded policy QA with retrieval benchmarking and source citations.')
class AskRequest(BaseModel):
    question:str=Field(min_length=2,max_length=2000)
    retriever:str='hybrid'
    k:int=Field(default=5,ge=1,le=20)
class AskResponse(BaseModel):
    answer:str; refused:bool; retriever:str; top_score:float; citations:list
@app.get('/health')
def health(): return {'status':'ok','service':'PolicyPilot'}
@app.post('/ask',response_model=AskResponse)
def ask_endpoint(payload:AskRequest):
    if payload.retriever not in ('bm25','embedding','hybrid'): raise HTTPException(400,'retriever must be bm25, embedding, or hybrid')
    try:
        result=ask(payload.question,payload.retriever,payload.k)
        result.pop('retrieved',None)
        return result
    except FileNotFoundError as e: raise HTTPException(503,str(e))
    except Exception as e: raise HTTPException(500,f'QA failed: {e}')
