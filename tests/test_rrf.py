from policypilot.retrievers import rrf

def d(i): return {'chunk_id':str(i),'text':str(i),'page_title':str(i)}
def test_rrf_promotes_consensus():
    ranked=rrf([[d(1),d(2),d(3)],[d(2),d(1),d(3)]],k=3)
    assert ranked[0]['chunk_id']=='1' or ranked[0]['chunk_id']=='2'
    assert ranked[0]['score']>ranked[-1]['score']
