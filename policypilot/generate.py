"""Grounded generation with source citation parsing; falls back to extractive response."""
import re, os
from .config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

SYSTEM_PROMPT='''You are PolicyPilot, a cautious handbook assistant. Answer only using the supplied passages. Do not use outside knowledge or infer policy. Cite every factual statement with passage citations like [1]. If the passages do not contain enough information, respond exactly or clearly with: I couldn't find this in the documents. Keep the answer concise. Never invent a citation.'''

def extractive_answer(question, passages):
    if not passages: return "I couldn't find this in the documents."
    # An intentionally conservative fallback: show the retrieved passage(s) rather than fabricate a synthesis.
    return 'I found these potentially relevant passages, but no LLM is configured to synthesize them:\n\n' + '\n\n'.join(f'[{i}] {p["text"][:700]}' for i,p in enumerate(passages,1))

def generate_answer(question, passages):
    if not LLM_API_KEY: return extractive_answer(question,passages)
    try:
        from openai import OpenAI
        client=OpenAI(api_key=LLM_API_KEY,base_url=LLM_BASE_URL)
        context='\n\n'.join(f'[{i}] Title: {p["page_title"]}\nSection: {p["section_path"]}\nURL: {p["url"]}\nPassage: {p["text"]}' for i,p in enumerate(passages,1))
        response=client.chat.completions.create(model=LLM_MODEL,temperature=0,max_tokens=450,messages=[{'role':'system','content':SYSTEM_PROMPT},{'role':'user','content':f'Question: {question}\n\nPassages:\n{context}'}])
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return f'Generation provider unavailable ({type(exc).__name__}). Retrieved passages are shown below.\n\n'+extractive_answer(question,passages)

def citation_ids(answer): return sorted(set(int(x) for x in re.findall(r'\[(\d+)\]',answer)))
