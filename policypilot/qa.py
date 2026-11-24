from .retrievers import search, load_index
from .refusal import should_refuse
from .generate import generate_answer, citation_ids

def ask(question,retriever='hybrid',k=5,threshold=None,index=None):
    if not question or not question.strip(): raise ValueError('Question must not be empty.')
    index=index or load_index()
    results=search(question,retriever,k,index)
    refused,top_score=should_refuse(results,retriever,threshold)
    if refused:
        answer="I couldn't find this in the documents."
        cited=[]
    else:
        answer=generate_answer(question,results)
        cited=citation_ids(answer)
    citations=[]
    for i,doc in enumerate(results,1):
        if refused or not cited or i in cited:
            citations.append({'citation_number':i,'title':doc['page_title'],'section':doc['section_path'],'url':doc['url'],'snippet':doc['text'][:600],'score':doc['score']})
    return {'answer':answer,'refused':refused,'retriever':retriever,'top_score':top_score,'citations':citations,'retrieved':results}
