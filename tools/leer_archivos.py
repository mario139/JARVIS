import os
from pypdf import PdfReader
from core.llm import hablar
import re

BASE = "data/documents"
MAX_CHARS = 6000
TROZO = 5000

def _limpiar(texto):
    texto = texto.replace("\r", "")
    texto = re.sub(r"\n{2,}", "\x00", texto)   # marca los párrafos reales
    texto = re.sub(r"\s*\n\s*", " ", texto)    # el resto de saltos -> espacio
    texto = texto.replace("\x00", "\n\n")      # devuelve los párrafos
    texto = re.sub(r"[ \t]{2,}", " ", texto)   # espacios dobles
    return texto.strip()


def _resolver(ruta):
    if not os.path.exists(ruta):
        ruta = os.path.join(BASE, ruta)
    return ruta


def _texto_completo(ruta):
    """Devuelve el texto entero del archivo (txt o pdf), sin cortar."""
    ruta = _resolver(ruta)
    if ruta.lower().endswith(".pdf"):
        lector = PdfReader(ruta)
        paginas = []
        for i, p in enumerate(lector.pages, 1):
            t = _limpiar(p.extract_text() or "").strip()
            if t:
                paginas.append(f"[Página {i}]\n{t}")
        if not paginas:
            raise ValueError("El PDF no tiene texto (puede ser escaneado)")
        return "\n\n".join(paginas)
    with open(ruta, "r", encoding="utf-8") as archi:
        return archi.read()


def leer_archivo(ruta):
    try:
        texto = _texto_completo(ruta)
    except (OSError, UnicodeDecodeError):
        return "No se pudo leer el archivo"
    except ValueError as e:
        return str(e)
    except Exception as e:  # PDF dañado, con contraseña, etc.
        return f"Error al leer el archivo: {e}"
    if len(texto) > MAX_CHARS:
        texto = texto[:MAX_CHARS] + (
            "\n[...archivo cortado. Para un documento largo usa resumir_documento...]"
        )
    return texto


def resumir_documento(ruta):
    try:
        texto = _texto_completo(ruta)
    except (OSError, UnicodeDecodeError):
        return "No se pudo leer el archivo"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Error al leer el archivo: {e}"

    trozos = [texto[i:i + TROZO] for i in range(0, len(texto), TROZO)]
    parciales = []
    for n, trozo in enumerate(trozos, 1):
        print(f"resumiendo parte {n}/{len(trozos)}...")
        parciales.append(hablar([
            {"role": "system", "content": "Resumes textos en español, de forma fiel y breve. No inventes nada que no esté en el texto."},
            {"role": "user", "content": f"Resume esta parte de un documento en 3-5 frases:\n\n{trozo}"},
        ]))

    if len(parciales) == 1:
        return parciales[0]

    union = "\n\n".join(f"Parte {i}: {p}" for i, p in enumerate(parciales, 1))
    return hablar([
        {"role": "system", "content": "Resumes textos en español, de forma fiel y breve. No inventes nada que no esté en el texto."},
        {"role": "user", "content": f"Estos son resúmenes de las partes de un mismo documento. Haz un resumen final claro y ordenado:\n\n{union}"},
    ])