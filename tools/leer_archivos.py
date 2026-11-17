def leer_archivo(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as archi:
            return archi.read()
    except OSError:
        return "No se pudo leer el archivo"