import sqlite3 # Importamos sqlite3, la version de sqlite para python, sirve para nuestra base de datos
from datetime import datetime
def inicializar():
    conexion = sqlite3.connect("data/memoria.db")
    cursor = conexion.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS recuerdos (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, texto TEXT, tipo TEXT)")
    conexion.commit()
    conexion.close()

def guardar(texto, tipo = "hecho"):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    conexion2 = sqlite3.connect("data/memoria.db")
    cursor = conexion2.cursor()
    cursor.execute("INSERT INTO recuerdos (fecha, texto, tipo) VALUES (?,?,?)",(fecha,texto,tipo))
    conexion2.commit()
    conexion2.close()
    return True

def listar(n=5):
    # Abrir la base de datos (el archivo data/memoria.db)
    conexion = sqlite3.connect("data/memoria.db")
    cursor = conexion.cursor()

    # Pedir los últimos n recuerdos:
    # - ORDER BY id DESC → primero los más nuevos
    # - LIMIT ? → solo n filas (el ? se rellena con n)
    cursor.execute(
        "SELECT id, fecha, texto, tipo FROM recuerdos ORDER BY id DESC LIMIT ?",
        (n,)
    )

    # Traer todas las filas que devolvió el SELECT
    # Cada fila es una tupla: (id, fecha, texto, tipo)
    filas = cursor.fetchall()

    # Cerrar la conexión (no hace falta commit: solo leímos)
    conexion.close()

    # Devolver la lista para que quien llame a listar() pueda usarla
    return filas
def buscar(palabra):
    contecion = sqlite3.connect("data/memoria.db")
    cursor = contecion.cursor() 
    cursor.execute("SELECT id, fecha, texto, tipo FROM recuerdos WHERE texto LIKE ?", (f"%{palabra}%",))
    resultado_busqueda = cursor.fetchall()
    contecion.close()
    return resultado_busqueda