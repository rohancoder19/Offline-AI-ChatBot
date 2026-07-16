import ollama

print("=="*50)
print("     powered by ollama llama3 model")
print("if you write exit , then progamme will be stopped")
print("=="*50)

while True:
    input_user=input("\n :::::  your input  :::::")

    if input_user.lower()=="exit":
        print("\n :::thanks for choose us::::")
        break
    response=ollama.chat(
        model="llama3",
        messages=[
            {
                "role":"user",
                "content":input_user
            }
        ]
    )



    print(response["message"]["content"])