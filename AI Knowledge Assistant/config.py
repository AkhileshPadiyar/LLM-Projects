import streamlit as st
import ollama
from sentence_transformers import SentenceTransformer
import chromadb

@st.cache_resource
def connect():
    return ollama.Client("http://127.0.0.1:11434")

@st.cache_resource
def get_sentence_transformer():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def get_db():
    return chromadb.PersistentClient(
        path = "./chromadb"
    )