from core.memory import listar

class Historial:
    def __init__(self, n_recuerdos=5):
        with open("prompt/system.txt", "r", encoding="utf-8") as archi:
            self.system_prompt = archi.read()

        recuerdos = listar(n_recuerdos)  # vienen del más nuevo al más viejo
        if recuerdos:
            recuerdos.reverse()  # ahora del más viejo al más nuevo (orden cronológico)
            lineas = []
            for id_, fecha, contenido, tipo in recuerdos:
                lineas.append(f"- [{fecha}] ({tipo}) {contenido}")
            bloque = "\n".join(lineas)
            self.system_prompt += (
                "\n\nRecuerdos de conversaciones anteriores:\n" + bloque
            )

        self.historial = [{"role": "system", "content": self.system_prompt}]

    def agregar_usuario(self, mensaje):
        self.historial.append({"role": "user", "content": mensaje})

    def agregar_asistente(self, respuesta):
        self.historial.append({"role": "assistant", "content": respuesta})

    def obtener_historial(self):
        return self.historial