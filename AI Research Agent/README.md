# AI Research Agent

An AI-powered research assistant that uses web search, LLMs, and agentic workflows to research topics, gather relevant information, and generate structured research reports.

## Features

- **Web Research:** Searches the web to gather relevant information.
- **LLM-Powered Responses:** Uses a locally hosted Mistral model through Ollama.
- **Agentic Workflow:** Uses LangGraph to manage research steps and execution flow.
- **Human-in-the-Loop:** Supports approval and continuation of workflow execution.
- **Chat History:** Stores conversations in SQLite.
- **Long-Term Memory:** Extracts and retrieves useful information from previous interactions.
- **Structured Reports:** Generates research reports using Pydantic schemas.
- **Checkpointing:** Uses LangGraph checkpointing to preserve workflow state.

## Tech Stack

- **Language:** Python
- **UI:** Streamlit
- **LLM:** Mistral 7B
- **LLM Runtime:** Ollama
- **Frameworks:** LangChain, LangGraph
- **Database:** SQLite
- **Data Validation:** Pydantic
- **Web Search:** DuckDuckGo Search
- **Deployment:** Docker (in progress)

## Tools and Libraries

- `langchain-ollama` — Connects the application to the local LLM.
- `langgraph` — Builds and manages agent workflows.
- `langgraph-checkpoint-sqlite` — SQLite-based workflow checkpointing.
- `duckduckgo-search` — Web search functionality.
- `streamlit` — Interactive research interface.
- `pydantic` — Structured output validation.
- `sqlite3` — Chat history and long-term memory storage.

## Workflow

1. The user submits a research question through the Streamlit interface.
2. The agent retrieves relevant memory and contextual information.
3. LangGraph manages the research workflow and tool execution.
4. The agent searches the web and gathers relevant information.
5. Human approval is requested when required by the workflow.
6. The LLM processes the collected information and generates a structured research report.
7. Chat history, long-term memory, and workflow state are managed through SQLite-based storage.

## Project Structure

```text
AI-Research-Agent/
├── app.py                  # Streamlit interface
├── main.py                 # Research execution and orchestration
├── agent.py                # LLM and agent configuration
├── workflow.py             # LangGraph workflow
├── config.py               # Database and chat configuration
├── Long_term_Memory.py     # Long-term memory management
├── schema.py               # Pydantic report schema
├── storage.py              # Database paths for persistence
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image configuration
├── compose.yaml            # Docker Compose configuration
└── README.md
```

## Setup and Run

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI-Research-Agent
```

### 2. Install dependencies

```bash
python -m venv venv
```

Activate the environment and install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Start Ollama

Install Ollama and ensure the Mistral model is available:

```bash
ollama pull mistral:7b-instruct
```

### 4. Run the application

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Future Improvements

- Dockerized deployment with persistent database storage.
- Improved source attribution and research quality.
- Enhanced memory retrieval and agent reliability.

---

**Built with Python, LangChain, LangGraph, Ollama, and Streamlit.**
