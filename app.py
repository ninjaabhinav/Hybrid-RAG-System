import streamlit as st
import os
from rag_service import RAGService
from config import Config

config = Config()
rag = RAGService()

st.set_page_config(page_title="Hybrid RAG System", layout="wide")

st.title("📚 Hybrid RAG System (Offline + Online)")

# Sidebar
st.sidebar.header("Document Management")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or PPT",
    type=["pdf", "ppt", "pptx"],
    accept_multiple_files=True
)

mode = st.sidebar.radio(
    "Mode",
    ["offline", "online"]
)

if uploaded_files:
    for file in uploaded_files:
        save_path = os.path.join(config.UPLOAD_DIR, file.name)

        with open(save_path, "wb") as f:
            f.write(file.read())

        st.sidebar.success(f"Saved: {file.name}")

        with st.spinner(f"Indexing {file.name}..."):
            rag.index_document(save_path)

    st.sidebar.success("Indexing complete.")

# Chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.divider()

user_input = st.chat_input("Ask a question about your documents...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("Generating answer..."):
        answer = rag.answer_query(user_input, mode=mode)

    st.session_state.chat_history.append(("assistant", answer))

# Display chat
for role, message in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.write(message)
    else:
        with st.chat_message("assistant"):
            st.write(message)