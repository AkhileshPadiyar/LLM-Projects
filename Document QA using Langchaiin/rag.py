import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
import os


@st.cache_resource
def load_file(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )

    return splitter.split_documents(documents)

@st.cache_resource
def create_embeddings():
    return HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )

@st.cache_resource
def create_vector_store(chunks, embeddings):
    vector_store = Chroma.from_documents(
        documents = chunks,
        embedding = embeddings,
        persist_directory = './chromadb'
    )
    return vector_store

def load_vector_store(embeddings):
    return Chroma(
        persist_directory = './chromadb',
        embedding_function=embeddings
    )
@st.cache_resource
def create_llm():
    return ChatOllama(
        model = (os.getenv("MODEL_NAME") or "mistral:7b-instruct"),
        temperature = 0
    )