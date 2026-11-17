from core.memory import inicializar, guardar, listar, buscar

inicializar()
print("BD inicializada")

guardar("Mario está construyendo Evee con Ollama")
guardar("Prefiere respuestas en español", tipo="preferencia")
print("Guardado OK")

print("Últimos recuerdos:")
print(listar(5))

print("Búsqueda 'Evee':")
print(buscar("Evee"))