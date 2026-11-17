from datetime import datetime
def obtener_Hora():
    Ahorita = datetime.now()
    formato = Ahorita.strftime("Fecha %d/%m/%Y Hora: %H:%M")
    return formato

