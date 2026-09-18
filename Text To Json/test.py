import ollama

response = ollama.chat(
    model='mistral:7b',
    messages=[{
        "role" : "user",
        "content" : "What is ollama",
    }]
)
print(response['message']['content'])