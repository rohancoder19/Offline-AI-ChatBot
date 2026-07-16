import ollama

response = ollama.chat(
    model="gemma2",
    messages=[
        {
                "role": "user",
                "content": "Hello, how are you?"
        }
    ]
)
print(response["message"]["content"])