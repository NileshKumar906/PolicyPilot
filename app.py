import streamlit as st
from policypilot.qa import ask
from policypilot.config import INDEX_PATH
st.set_page_config(page_title='PolicyPilot',page_icon='📘',layout='wide')
st.title('📘 PolicyPilot')
st.caption('Grounded handbook Q&A · Retrieval benchmarking · Citation-aware answers')
if not INDEX_PATH.exists():
    st.warning('No index yet. Fetch the corpus and build the index using the setup steps in README. You can also run the demo corpus index.')
with st.sidebar:
    st.header('Retrieval settings')
    retriever=st.selectbox('Strategy',['hybrid','bm25','embedding'])
    k=st.slider('Passages to retrieve',1,10,5)
    st.caption('Refusal threshold is experimental and should be tuned on a development split.')
if 'messages' not in st.session_state: st.session_state.messages=[]
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])
        if msg.get('citations'):
            for c in msg['citations']:
                with st.expander(f"Source: {c['title']} · {c.get('section','')}"):
                    st.write(c['snippet']); st.markdown(f"[Open handbook page]({c['url']})")
question=st.chat_input('Ask about a policy...')
if question:
    st.session_state.messages.append({'role':'user','content':question})
    with st.chat_message('user'): st.markdown(question)
    with st.chat_message('assistant'):
        try:
            with st.spinner('Searching and checking evidence...'):
                result=ask(question,retriever,k)
            st.markdown(result['answer'])
            if result['refused']: st.info('Refusal gate activated: retrieved evidence was below the configured threshold.')
            else: st.caption(f"Retriever: {retriever} · top score: {result['top_score']:.4f}")
            for c in result['citations']:
                with st.expander(f"Source: {c['title']} · {c.get('section','')}"):
                    st.write(c['snippet']); st.markdown(f"[Open handbook page]({c['url']})")
            st.session_state.messages.append({'role':'assistant','content':result['answer'],'citations':result['citations']})
        except Exception as e:
            st.error(str(e))
