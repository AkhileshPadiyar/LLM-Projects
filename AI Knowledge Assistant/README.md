# AI Knowledge Assistant

A local document Q&A app built with Streamlit, Ollama, embeddings, and ChromaDB.

It lets you upload documents, search their content using semantic search, and ask questions about them.

## Features

- Supports TXT and PDF files
- Splits documents into chunks
- Creates embeddings using Sentence Transformers
- Stores embeddings in ChromaDB
- Finds relevant chunks using semantic search
- Uses Ollama for local LLM responses
- Keeps chat history
- Supports multiple documents
- Detects duplicate documents
- Allows document deletion
- Returns structured responses using Pydantic

## Tech Stack

- Python
- Streamlit
- Ollama
- Mistral
- Sentence Transformers
- ChromaDB
- PyMuPDF
- Pydantic

## How It Works

```text
Document
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embeddings
   ↓
ChromaDB
   ↓
User Question
   ↓
Query Embedding
   ↓
Semantic Search
   ↓
Relevant Chunks
   ↓
Ollama + Mistral
   ↓
Answer
```

## Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Ollama

Make sure Ollama is running and the required model is available.

```bash
ollama run mistral
```

### 3. Start the app

```bash
streamlit run app.py
```

## Project Structure

```text
AI-Knowledge-Assistant/
├── app.py
├── config.py
├── document.py
├── chunker.py
├── llm.py
├── schema.py
├── embeddings/
│   └── embedder.py
└── chromadb/
```
