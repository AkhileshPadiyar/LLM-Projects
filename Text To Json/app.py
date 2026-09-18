import streamlit as st
import ollama
from pydantic import BaseModel
from typing import Optional, List
from dynamic_pydantic import create_dynamic_model
import json
from validator import validate

st.title("Text to JSON")

text = st.text_area("Enter the text", placeholder="I am akhilesh and ...")


schema_input = st.text_area(
    "Define the fields to extract",
    value="""{
    "customer_name": "string",
    "product": "string",
    "price": "number",
    "order_date": "string",
    "order_id": "string"
}""",
    height=200
)


client = ollama.Client(host="http://127.0.0.1:11434")

dummy = """
            Hello i am akhilesh and i am student of graphic era deemed to be University.
            I am currently pusing B.tech in Computer science and engineering.
            I am skilled in javascript, react, python
        """

# if st.button("Convert to JSON"):
#     if not text.strip():
#         st.warning("Please enter some text to convert")
#         st.stop()
#     if not schema_input.strip():
#         st.warning("Please enter some schema to convert")
#         st.stop()
#
#     try:
#         schema = json.loads(schema_input)
#     except json.JSONDecodeError:
#         st.warning("Plese enter a valid JSON")
#         st.stop()
#
#     dynamic_model = create_dynamic_model(schema)
#
#
#     prompt = f"""
#     You are a data extraction system.
#
#     Extract information from the provided text.
#
#     Return ONLY valid JSON.
#
#     The output MUST follow this schema:
#
#     {json.dumps(schema, indent=2)}
#
#     Rules:
#     - Do not add fields that are not present in the schema.
#     - Use null when information cannot be found.
#     - Follow the requested data types.
#     - Do not hallucinate information.
#     - Do not provide explanations.
#     - Do not use markdown.
#     - Return ONLY the JSON object.
#
#     Text:
#     {text}
#     """
#
#     st.write(json.dumps(schema, indent = 10))
#
#     try:
#         response = client.chat(
#             model = "mistral:7b",
#             messages = [
#             {
#                 "role" : "user",
#                 "content" : prompt,
#             }
#         ],
#             options = {
#                 "temperature" : 0,
#             }
#         )
#         result = response['message']['content']
#
#         st.subheader("Raw LLM Response")
#         st.markdown(result)
#
#         try:
#             data = json.loads(result)
#             data = dynamic_model(**data)
#
#             st.subheader("Validated JSON Response")
#             st.json(data.model_dump())
#         except json.JSONDecodeError:
#             st.error("The model returned an invalid JSON")
#         except Exception as e:
#             st.error(e)
#
#
#     except Exception as e:
#         st.error("Failed to load JSON ", e)

if st.button("Convert to JSON"):
    with st.spinner("Generating Response"):
        validate(client, text, schema_input)



