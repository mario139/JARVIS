import re
from core.llm import chat, hablar
from tools.Herramientas import Herr
from tools.hora import obtener_Hora
from tools.leer_archivos import leer_archivo
from core.memory import guardar, buscar, listar
from tools.subagentes import delegar

HERRAMIENTAS = {
    "obtener_hora": obtener_Hora,
    "leer_archivo": leer_archivo,
    "guardar_memoria": guardar,
    "buscar_memoria": buscar,
    "listar_memoria": listar,
    "delegar":delegar,
}

PIDE_HORA = re.compile(
    r"\b(qu[eé] hora|la hora|qu[eé] fecha|la fecha de hoy|qu[eé] d[ií]a)\b"
)


def formatear(resultado):
    if isinstance(resultado, bool):
        return "Guardado correctamente." if resultado else "No se pudo guardar."
    if isinstance(resultado, list):
        if not resultado:
            return "No encontré recuerdos."
        return "\n".join(f"- [{f}] ({t}) {x}" for _, f, x, t in resultado)
    return str(resultado) if resultado is not None else "OK"


def ejecutar_herramienta(llamada):
    nombre = llamada["function"]["name"]
    argumentos = llamada["function"].get("arguments", {})
    if nombre not in HERRAMIENTAS:
        return nombre, f"Error: la herramienta '{nombre}' no existe"
    try:
        resultado = HERRAMIENTAS[nombre](**argumentos)
    except Exception as error:  # el modelo a veces manda argumentos mal
        resultado = f"Error al ejecutar {nombre}: {error}"
    #print("tool:", nombre, "resultado:", resultado)
    return nombre, formatear(resultado)


def responder(e):
    mensaje = chat(e, Herr)
    llamadas = mensaje.get("tool_calls")

    if llamadas:
        lista2 = e.copy()
        lista2.append({
            "role": "assistant",
            "content": mensaje.get("content") or "",
            "tool_calls": llamadas,
        })
        directo = []
        for llamada in llamadas:
            nombre, resultado = ejecutar_herramienta(llamada)
            lista2.append({"role": "tool", "name": nombre, "content": resultado})
            if nombre == "delegar":
                directo.append(resultado)
        if directo:
            return "\n\n".join(directo)
        return chat(lista2, Herr)["content"]

    # Sin tools: ¿parece pregunta de hora/fecha?
    texto_usuario = ""
    for m in reversed(e):
        if m.get("role") == "user":
            texto_usuario = m.get("content", "").lower()
            break

    if PIDE_HORA.search(texto_usuario):
        resultado = obtener_Hora()
        print("TOOL FORZADA: obtener_hora →", resultado)
        mensajes_hora = e.copy()
        mensajes_hora.append({
            "role": "user",
            "content": (
                "El usuario preguntó la hora o la fecha. "
                f"Resultado de la herramienta obtener_hora: {resultado}. "
                "Responde en lenguaje natural con ese dato. "
                "No inventes otra hora."
            ),
        })
        return hablar(mensajes_hora)

    return mensaje["content"]


def cerrar_sesion(historial):
    """Resume la sesión y la guarda. Se salta system (0) y el repaso inicial (1 y 2)."""
    if len(historial) <= 3:  # el usuario no dijo nada, no hay qué resumir
        return None
    pedido = [historial[0]] + historial[3:] + [{
        "role": "user",
        "content": (
    "Resume en 2 o 3 frases SOLO lo que el usuario dijo, decidió o dejó "
    "pendiente. Distingue bien: si el usuario preguntó o mostró curiosidad, "
    "escribe 'preguntó por X' o 'quiere saber sobre X', NUNCA 'prefiere' ni "
    "'decidió'. No incluyas preguntas que hizo el asistente ni explicaciones "
    "técnicas. Solo el resumen, sin saludos."
),
    }]
    resumen = hablar(pedido)
    guardar(resumen, "resumen")
    return resumen