# 📄 AI Document Q&A

A local **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents and ask questions about their content.

The application extracts information from the uploaded document, converts the document chunks into embeddings, stores them in a persistent ChromaDB vector database, retrieves the most relevant chunks for a user's question, and uses a local LLM through Ollama to generate the answer.

---

## ✨ Features

* 📄 Upload PDF documents through a Streamlit interface
* ✂️ Automatically chunk document content
* 🧠 Generate semantic embeddings using Sentence Transformers
* 🔍 Perform semantic similarity search using ChromaDB
* 🤖 Generate answers using a local Ollama LLM
* ♻️ Detect duplicate documents using SHA-256 hashing
* 💾 Persist embeddings and document chunks locally
* ⚡ Cache expensive resources using Streamlit's `st.cache_resource`
* 🔒 Run the complete application locally without external LLM APIs

---

## 🛠️ Tech Stack

| Component            | Technology                  |
| -------------------- | --------------------------- |
| Programming Language | Python                      |
| User Interface       | Streamlit                   |
| PDF Processing       | PyMuPDF                     |
| Embedding Model      | `all-MiniLM-L6-v2`          |
| Embedding Framework  | Sentence Transformers       |
| Vector Database      | ChromaDB                    |
| LLM Runtime          | Ollama                      |
| LLM                  | Configurable through `.env` |
| Storage              | Local ChromaDB              |

---

## 🏗️ Project Structure

```text
AI-Document-QA/
│
├── app.py                 # Streamlit UI and application entry point
├── ingestion.py           # Document ingestion pipeline
├── chunking.py             # PDF text extraction and chunk generation
├── retrieval.py            # Query embedding, retrieval and answer generation
├── vector_store.py         # ChromaDB storage and semantic search
├── rag.py                  # Prompt construction and LLM response generation
│
├── chromadb/               # Persistent ChromaDB storage
├── .env                    # Environment variables
└── README.md
```

---

## 🔄 How It Works

The application follows a basic RAG pipeline:

```text
                     PDF
                      │
                      ▼
               Text Extraction
                      │
                      ▼
                  Chunking
                      │
                      ▼
             Sentence Transformer
                  Embeddings
                      │
                      ▼
                 ChromaDB
                      │
                      │
            ┌─────────┴─────────┐
            │                   │
            ▼                   │
      User Question             │
            │                   │
            ▼                   │
      Query Embedding           │
            │                   │
            ▼                   │
      Similarity Search ────────┘
            │
            ▼
      Relevant Chunks
            │
            ▼
       Prompt + Context
            │
            ▼
         Ollama LLM
            │
            ▼
          Answer
```

### 1. PDF Upload

The user uploads a PDF through Streamlit.

The application reads the PDF bytes and generates a SHA-256 hash:

```text
PDF
 ↓
SHA-256
 ↓
Document ID
```

This ID is used to determine whether the document has already been processed.

---

### 2. Document Ingestion

For a new document:

```text
PDF
 ↓
Chunking
 ↓
Embedding Generation
 ↓
ChromaDB
```

The document is divided into smaller chunks using the project's chunking logic.

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The resulting embeddings, chunks, and metadata are stored in ChromaDB.

---

### 3. Duplicate Detection

Before processing a document, its SHA-256 hash is checked against the existing documents.

```text
New PDF
   ↓
Generate SHA-256
   ↓
Check ChromaDB
   │
   ├── Already exists → Skip processing
   │
   └── New document → Process and store
```

This prevents the same PDF from being embedded and stored repeatedly.

---

### 4. Question Retrieval

When the user asks a question:

```text
Question
   ↓
Embedding Model
   ↓
Query Vector
   ↓
ChromaDB
   ↓
Top 3 Relevant Chunks
```

The question is converted into an embedding and compared against the stored document embeddings.

The application retrieves the three most relevant chunks by default.

---

### 5. Answer Generation

The retrieved chunks are combined into a context and passed to the LLM.

The prompt instructs the model to answer using the provided document context.

```text
Relevant Chunks
      +
User Question
      ↓
     Prompt
      ↓
  Ollama / LLM
      ↓
   Final Answer
```

If the answer cannot be found in the retrieved context, the model is instructed to state that it could not find the answer in the document.

---

## 🧩 Core Components

### `app.py`

The main application entry point.

Responsible for:

* Streamlit interface
* PDF upload
* Document hashing
* Session state
* Resource caching
* Connecting ingestion and retrieval

---

### `ingestion.py`

Handles document ingestion.

```text
PDF
 ↓
Check duplicate
 ↓
Generate chunks
 ↓
Generate embeddings
 ↓
Store in ChromaDB
```

---

### `chunking.py`

Responsible for extracting/processing PDF content and generating chunks that can be embedded and searched.

---

### `vector_store.py`

Handles ChromaDB operations:

* Checking whether a document exists
* Storing chunks
* Storing embeddings
* Storing metadata
* Performing similarity search

Each chunk is stored with metadata such as:

```text
document_id
chunk_index
```

---

### `retrieval.py`

Handles the query pipeline:

```text
Question
 ↓
Question Embedding
 ↓
Vector Search
 ↓
Relevant Chunks
 ↓
LLM Answer
```

---

### `rag.py`

Responsible for the actual **Generation** part of RAG.

It:

1. Combines retrieved chunks into context.
2. Builds the prompt.
3. Sends the prompt to Ollama.
4. Returns the generated answer.

---

## 💾 Data Stored in ChromaDB

Each document chunk is stored with:

```text
ID
Document Text
Embedding Vector
Metadata
```

Example:

```text
document_id_chunk_0

Embedding:
[0.023, -0.184, 0.731, ...]

Metadata:
{
    "document_id": "...",
    "chunk_index": 0
}
```

ChromaDB is persisted locally in:

```text
./chromadb
```

---

## ⚡ Performance Optimizations

### Streamlit Session State

The application uses:

```python
st.session_state
```

to remember the currently processed document.

This prevents document ingestion from happening again when Streamlit reruns the application after a question is submitted.

### Resource Caching

The embedding model and Ollama client are loaded through:

```python
@st.cache_resource
```

This prevents expensive resources from being initialized repeatedly during Streamlit reruns.

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI-Document-QA
```

### 2. Create and activate a virtual environment

For Conda:

```bash
conda create -n document-qa python=3.11
conda activate document-qa
```

### 3. Install dependencies

```bash
pip install streamlit ollama sentence-transformers chromadb pymupdf python-dotenv
```

### 4. Install Ollama

Install Ollama and download the LLM you want to use.

For example:

```bash
ollama pull mistral:7b
```

### 5. Configure `.env`

Create a `.env` file:

```env
MODEL_NAME=mistral:7b
```

The model name is read by `rag.py`.

### 6. Run the application

```bash
streamlit run app.py
```

---

## 🚀 Usage

1. Start the application.
2. Upload a PDF.
3. Wait for the document to be processed.
4. Enter a question about the document.
5. The application retrieves relevant content.
6. The local LLM generates the answer.

Example:

```text
Question:
What are the main causes of overfitting?

Answer:
[Answer generated using the retrieved document context]
```

---

## 🧠 Concepts Demonstrated

This project provides hands-on implementation of several important GenAI concepts:

* Retrieval-Augmented Generation (RAG)
* Document ingestion
* PDF text extraction
* Text chunking
* Semantic embeddings
* Vector databases
* Similarity search
* Prompt engineering
* Local LLM inference
* Ollama
* Streamlit session state
* Resource caching
* Document deduplication

---

## 🔮 Future Improvements

Possible extensions include:

* 📑 Page-level source citations
* 💬 Conversational chat history
* 📚 Multiple PDF support
* 🏷️ Improved metadata and metadata filtering
* 🎯 Similarity score thresholds
* 🔄 Better semantic chunking
* 🔎 Hybrid keyword + vector search
* 🧠 Reranking retrieved chunks
* ⚡ Streaming LLM responses
* 🗑️ Document management and deletion
* 📊 Retrieval evaluation and quality metrics

---

## 📌 RAG in One Line

```text
Document → Chunk → Embed → Store → Retrieve → Augment → Generate
```

The goal of this project is to understand the **fundamentals of building a RAG application from scratch**, without hiding the core retrieval and generation process behind a high-level framework.
