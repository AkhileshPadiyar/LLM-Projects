from config import connect
import json
from schema import RagResponse
from pydantic import ValidationError

def generate_answer(model_name, system_prompt, question):
    client = connect()
    response = client.chat(
        model = model_name,
        messages = [
            {
                "role" : "system",
                "content" : system_prompt
            },
            {
                "role" : "user",
                "content" : question
            }
        ],
        options={
            "temperature" : 0
        }
    )

    return response['message']['content']

def generate_rag_answer(documents, question, model_name, system_prompt, chat_history):
    prev_conversation = ""
    for chat in chat_history:
        prev_conversation += f"role : {chat['role']}\nContent: {chat['content']}\n"

    system_prompt = f"""
    Follow these instruction while generating the response
    - Return only JSON
    - Use exactly these fields:
        answer
        confidence
        sources
    - confidence must be a number between 0 and 1
    - sources must be a list of filenames
    - Do not wrap the JSON in Markdown code fences.
        \n
        {system_prompt}
     """
    prompt = f"""
        Answer the questions based on the previous conversations and context provided.
        Donot add any information of your own.
        If not able to find answer, return Cannnot find the answer from the files provided
        Previous Conversation: {prev_conversation}
        Context : {documents}
        Question: {question}
    """

    client = connect()

    response = client.chat(
        model = model_name,
        messages = [
            {
                "role" : "system",
                "content" : system_prompt
            },
            {
                "role" : "user",
                "content" : prompt
            }
        ],
        options = {
            "temperature" : 0
        }
    )

    result = response['message']['content']
    try:
        data = json.loads(result)
        validated_response = RagResponse(**data)
        return validated_response
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON genereated by LLM : {e}")
    except ValidationError as e:
        raise ValueError(f"Generated JSON doesn't match the schema : {e}")
