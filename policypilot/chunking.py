"""Markdown section-aware chunking utilities."""
import re
from typing import Iterable

TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)

def approx_tokens(text: str) -> int:
    return len(TOKEN_RE.findall(text))

def split_long_text(text: str, max_tokens: int = 320, overlap: int = 45) -> list[str]:
    words = text.split()
    if not words: return []
    # Word windows are used as a deterministic, dependency-free token approximation.
    window = max(50, int(max_tokens * 0.72))
    stride = max(1, window - int(overlap * 0.72))
    pieces=[]
    for start in range(0, len(words), stride):
        piece=' '.join(words[start:start+window]).strip()
        if piece: pieces.append(piece)
        if start+window >= len(words): break
    return pieces

def section_chunks(markdown: str, page_title: str, url: str, source_path: str = '', max_tokens: int = 320, overlap: int = 45) -> list[dict]:
    text=markdown.replace('\r\n','\n')
    text=re.sub(r'^---\\n.*?\\n---\\n','',text,flags=re.S)
    # Build sections based on H2/H3, preserving the full heading path.
    lines=text.splitlines(); current=[]; path=[]; sections=[]
    for line in lines:
        m=re.match(r'^(#{2,3})\s+(.*)$', line)
        if m:
            if current: sections.append((list(path), '\n'.join(current).strip()))
            level=len(m.group(1)); heading=m.group(2).strip()
            path=path[:level-2]; path.append(heading); current=[]
        else: current.append(line)
    if current: sections.append((list(path), '\n'.join(current).strip()))
    if not sections and text.strip(): sections=[([],text.strip())]
    result=[]
    for section_path, body in sections:
        if not body: continue
        for piece in split_long_text(body,max_tokens,overlap):
            result.append({'chunk_id':'','page_title':page_title,'section_path':' > '.join(section_path),'url':url,'source_path':source_path,'text':piece})
    return result
