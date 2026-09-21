import streamlit as st
import ollama
from sentence_transformers import SentenceTransformer
from ingestion import ingest_document
import hashlib
from retrieval import retrieve_chunks


# pdf -> pdf read(store in temp.pdf) -> chunks -> embedding -> vector_database

if "document_id" not in st.session_state:
    st.session_state.document_id = None
if "document_processed" not in st.session_state:
    st.session_state.document_processed = False

@st.cache_resource
def load_resources():
    client = ollama.Client("http://127.0.0.1:11434")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return client, model

client,model = load_resources()

st.title("AI Document QA")

pdf = st.file_uploader("Upload a file", type = ['pdf'])


def generate_document_id(pdf_bytes):
    return hashlib.sha256(pdf_bytes).hexdigest()

if pdf:
    st.write("PDF is uploading...")
    pdf_bytes = pdf.getvalue()

    document_id = generate_document_id(
        pdf_bytes
    )

    if st.session_state.document_id != document_id:
        status_container = st.status("Processing the file: ", expanded=True)

        st.session_state.document_id = document_id
        st.session_state.document_processed = True

        processed = ingest_document(pdf, document_id, model, status_container)
        if processed:
            status_container.update(label="✅ Document Processed succesfully..", state='complete', expanded=False)
        else:
            status_container.update(label="Document already exists", state='complete', expanded=False)


if st.session_state.document_processed:
    question = st.text_input(
        "Ask a question about the document"
    )

    if question:
        answer = retrieve_chunks(
            question, model
        )

        st.markdown("### Answer")

        st.write(answer)






