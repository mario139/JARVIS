import ollama

SUBAGENTES = {
    "programador": {
        "modelo": "qwen2.5-coder:7b",
        "system": "Eres un programador experto. Responde en español, con el código en bloques y una explicación corta.",
    },
}

def delegar(agente, tarea):
    cfg = SUBAGENTES.get(agente)
    if not cfg:
        return f"No existe el subagente '{agente}'. Disponibles: {', '.join(SUBAGENTES)}"
    r = ollama.chat(
        model=cfg["modelo"],
        messages=[
            {"role": "system", "content": cfg["system"]},
            {"role": "user", "content": tarea},
        ],
    )
    return r["message"]["content"]