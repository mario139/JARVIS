import ollama

MODELO = "qwen2.5:7b"

def chat(mensajes, herramientas=None):
    """Llamada a Ollama. Devuelve el mensaje completo (con tool_calls si hay)."""
    if herramientas:
        respuesta = ollama.chat(model=MODELO, messages=mensajes, tools=herramientas)
    else:
        respuesta = ollama.chat(model=MODELO, messages=mensajes)
    return respuesta["message"]

def hablar(mensajes):
    """Solo texto, sin herramientas."""
    return chat(mensajes)["content"]