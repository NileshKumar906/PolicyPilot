from policypilot.chunking import section_chunks,split_long_text

def test_no_empty_chunks_and_metadata():
    chunks=section_chunks('# Demo\n\n## Section\n\nSome policy text.','Demo','https://example.com')
    assert chunks and all(c['text'].strip() for c in chunks)
    assert all('page_title' in c and 'url' in c and 'section_path' in c for c in chunks)

def test_long_text_is_split():
    chunks=split_long_text('word '*1000,max_tokens=220,overlap=30)
    assert len(chunks)>1
