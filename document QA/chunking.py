import fitz
import streamlit as st

def generate_chunks(pdf):
    with open('temp.pdf', 'wb') as file:
        file.write(pdf.getbuffer())
    document = fitz.open('temp.pdf')
    text = ""
    for page in document:
        text+=page.get_text()
    document.close()
    # st.write(f'current len : {len(text)}')

    chunks = []
    chunk_size = 500
    overlap = 50

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks