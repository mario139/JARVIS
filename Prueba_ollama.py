import ollama
from ollama import chat

response = ollama.chat(
    model="qwen3:8b",
    messages=[
        {"role": "user", "content": "Hola, ¿puedes presentarte en una frase?"}
    ]
)

print(response["message"]["content"])