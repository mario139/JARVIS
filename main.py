from core.memory import inicializar, guardar
from core.history import Historial
from core.agent import responder, cerrar_sesion

inicializar()
historial = Historial()

# Repaso inicial: la IA habla primero
historial.agregar_usuario(
    "Inicia la sesión: haz un repaso breve y natural de lo que recuerdas "
    "de nuestra última conversación, y pregúntame en qué seguimos."
)
saludo = responder(historial.obtener_historial())
historial.agregar_asistente(saludo)
print(saludo)

while True:
    try:
        pregunta = input("Mensaje: ")
    except (KeyboardInterrupt, EOFError):  # Ctrl+C también cierra bien
        break

    if pregunta.lower() == "break":
        break
    elif pregunta.lower().startswith("recuerda:"):
        guardar(pregunta[len("recuerda:"):].strip())
        print("Guardado.")
    else:
        historial.agregar_usuario(pregunta)
        h = responder(historial.obtener_historial())
        historial.agregar_asistente(h)
        print(h)

resumen = cerrar_sesion(historial.obtener_historial())
if resumen:
    print("\nResumen guardado:", resumen)