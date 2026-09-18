import requests

def summarizer_text(text, style, temp):
    prompt = f"""
    You are a text summarizer assisstant

    Summarise the following text clearly and concisely into {style}
    Keep the important facts and remove unneccessary details.

    Text:
    {text}

    Summary:
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral:7b",
            "prompt" : prompt,
            "stream":False,
            "options" : {
                "temprature" : temp
            }
        }
    )

    return response.json()['response']