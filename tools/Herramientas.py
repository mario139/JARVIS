Herr = [
    {
    "type" : "function", 
    "function":{
    "name": "obtener_hora",
    "description":"Obtiene la fecha y la hora actual del sistema. Usala SIEMPRE que el usuario te pida la hora o la fecha, no inventes la hora ni la fecha, siempre usa esta herramienta para obtenerla",
    "parameters":{
        "type" : "object",
        "properties":{},
        "required":[]
    }
}
},
{
  "type": "function",
  "function":{
      "name": "leer_archivo",
      "description": "Lee el archivo dado y devuelve el texto",
      "parameters":{
          "type": "object",
          "properties":{
              "ruta":{
                  "type":"string",
                  "description": "Ruta del archivo a leer"
              }
          },
         "required":["ruta"]
      }
  }  
},
{
    "type": "function",
    "function":{
        "name": "guardar_memoria",
        "description": "Guarda un texto en la memoria de Evee. Úsala para guardar información importante que pueda ser útil en el futuro, como preferencias del usuario, hechos relevantes o cualquier dato que deba recordarse.",
        "parameters":{
            "type": "object",
            "properties":{
                "texto":{
                    "type":"string",
                    "description": "Texto a guardar en la memoria"
                },
                "tipo": {
                        "type": "string",
                        "description": "Categoría: hecho, preferencia, pendiente o proyecto"
                    }
            },
             "required":["texto"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "buscar_memoria",
        "description": "Busca en la memoria a largo plazo recuerdos que contengan una palabra o frase. Úsala cuando el usuario pregunte qué recuerdas sobre algo o pida buscar en la memoria.",
        "parameters": {
            "type": "object",
            "properties": {
                "palabra": {
                    "type": "string",
                    "description": "Palabra o frase a buscar dentro de los recuerdos guardados"
                }
            },
            "required": ["palabra"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "listar_memoria",
        "description": "Lista los recuerdos más recientes de la memoria a largo plazo. Úsala cuando el usuario pregunte qué recuerdas en general o pida ver los últimos recuerdos.",
        "parameters": {
            "type": "object",
            "properties": {
                "n": {
                    "type": "integer",
                    "description": "Cantidad de recuerdos recientes a mostrar (por defecto 5)"
                }
            },
            "required": []
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "delegar",
        "description": "Delega una tarea a un modelo especialista. Usa 'programador' para escribir, corregir o explicar código. Incluye en 'tarea' todo el contexto necesario, porque el especialista no ve la conversación.",
        "parameters": {
            "type": "object",
            "properties": {
                "agente": {"type": "string", "enum": ["programador"]},
                "tarea": {"type": "string", "description": "Instrucción completa y con contexto"},
            },
            "required": ["agente", "tarea"],
        },
    },
},
{
    "type": "function",
    "function": {
        "name": "resumir_documento",
        "description": "Resume un documento completo (PDF o texto), incluso si es largo. Úsala cuando el usuario pida un resumen de un archivo. Para leer solo un archivo corto usa leer_archivo.",
        "parameters": {
            "type": "object",
            "properties": {
                "ruta": {"type": "string", "description": "Nombre o ruta del archivo (se busca también en data/documents)"}
            },
            "required": ["ruta"]
        }
    }
},
]