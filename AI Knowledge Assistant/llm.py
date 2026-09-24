from config import connect

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

    return response['message']['content']