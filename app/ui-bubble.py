import streamlit as st
from search import search
from rag_chain import ask

st.set_page_config(page_title="Chat with Docs", page_icon="📄")
st.title("🧠 Chat with Your AWS Docs")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask something about AWS...")

if user_input:
    with st.spinner("Searching and generating response..."):
        retriever = search(user_input)
        response = ask(user_input, retriever=retriever)

    st.session_state.chat_history.append({"user": user_input, "bot": response})

# Render conversation bubbles
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["user"])
    with st.chat_message("assistant"):
        st.markdown(chat["bot"])
