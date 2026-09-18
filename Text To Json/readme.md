# AI Text → JSON Extractor

A simple GenAI application that converts **unstructured text into structured JSON** using a locally running **Mistral 7B model through Ollama**.

The user defines the fields they want to extract, and the application dynamically creates a **Pydantic model** to validate the LLM's response.

## Tech Stack

* Python
* Streamlit
* Ollama
* Mistral 7B
* Pydantic

## How It Works

```text
User Text + JSON Schema
          ↓
     Prompt Builder
          ↓
       Mistral 7B
          ↓
       JSON Response
          ↓
      JSON Parsing
          ↓
 Dynamic Pydantic Model
          ↓
       Validation
          ↓
    Validated JSON
```

## Project Structure

```text
Text To Json/
│
├── app.py
├── validator.py
├── dynamic_pydantic.py
└── README.md
```

### `app.py`

Handles the Streamlit UI and Ollama client.

* Takes text from the user
* Takes the extraction schema
* Calls the validation/extraction pipeline

### `validator.py`

Contains the main extraction and validation logic.

* Validates user input
* Converts the schema from JSON string to Python dictionary
* Creates the dynamic Pydantic model
* Builds the LLM prompt
* Calls Mistral through Ollama
* Parses the LLM response
* Validates the response using Pydantic

### `dynamic_pydantic.py`

Dynamically creates a Pydantic model from the user's schema.

Currently supports:

```text
string
integer
number
boolean
list[string]
```

## Example

### Input Text

```text
Rahul purchased an iPhone 15 for ₹65,000
on September 15, 2026. His order ID is ORD-98231.
```

### Schema

```json
{
  "customer_name": "string",
  "product": "string",
  "price": "number",
  "order_date": "string",
  "order_id": "string"
}
```

### Output

```json
{
  "customer_name": "Rahul",
  "product": "iPhone 15",
  "price": 65000,
  "order_date": "September 15, 2026",
  "order_id": "ORD-98231"
}
```

## Setup

### 1. Install dependencies

```bash
pip install streamlit ollama pydantic
```

### 2. Make sure Ollama is running

Check the model:

```bash
ollama list
```

The project uses:

```text
mistral:7b
```

### 3. Run the application

```bash
python -m streamlit run app.py
```

## Key Concepts Learned

* Calling a local LLM with Ollama
* Prompt engineering for structured output
* JSON parsing with `json.loads()`
* JSON serialization with `json.dumps()`
* Dynamic Pydantic models
* Runtime data validation
* Python dictionary unpacking with `**`
* Converting Pydantic models using `model_dump()`

## Current Limitations

* No automatic JSON repair/retry yet
* Nested JSON schemas are not supported
* Extraction depends on the LLM producing usable JSON

## Future Improvements

* Automatic JSON repair
* Retry mechanism
* Nested schema support
* More JSON Schema types
* FastAPI backend
* JSON/file download
