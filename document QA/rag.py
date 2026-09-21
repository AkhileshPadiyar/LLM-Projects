import ollama
from dotenv import load_dotenv
import os

load_dotenv()


def generate_answer(relevant_chunks, question):
    context = '\n\n'.join(relevant_chunks)

    prompt = f"""
                    You are a helpful document assistant
                    Answer the user's questions using only the information provided
                    in the context below

                    if the answer cannot be found in the context, say:
                    "I couldn't find the answer in the document'

                    Context: 
                    {context}
                    
                    Question:
                    {question}

                    Answer:
                    """

    response = ollama.chat(
        model=os.getenv("MODEL_NAME"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response['message']['content']
    return result