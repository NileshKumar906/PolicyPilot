from fastapi.testclient import TestClient
from api import app
client=TestClient(app)
def test_health():
    r=client.get('/health'); assert r.status_code==200 and r.json()['status']=='ok'
def test_invalid_retriever():
    r=client.post('/ask',json={'question':'What is policy?','retriever':'bad','k':5}); assert r.status_code==400
