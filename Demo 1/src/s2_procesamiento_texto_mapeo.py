import spacy
import re
from datetime import datetime
import locale
import json
import os

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

nlp = spacy.load('es_core_news_sm')
# with open("transcripcion.txt", "r") as archivo:
#     texto = archivo.read()
# texto = "El paciente es Javier Ríos, nacido el 26 de Diciembre de 2003, con diagnóstico de diabetes mellitus tipo 2. Su correo es javier.algo@gmail.com y su teléfono es 123456789. Su próxima revisión será el 27 de Junio de 2026"
# doc = nlp(texto)


def procesar_texto(ruta_transcripcion, ruta_salida) -> None:
    '''
    Dado un texto extraído de una transcripción de audio, extrae los datos relevantes del paciente y los exporta a un archivo JSON
    '''
    with open(ruta_transcripcion, "r") as archivo:
        texto = archivo.read()

    doc = nlp(texto)

    # Variables para los datos
    nombre = ""
    fecha_nacimiento = ""
    correo = ""
    telefono = ""
    diagnostico = ""
    proxima_cita = ""

    # NER
    for ent in doc.ents:
        if ent.label_ == "PER":
            nombre = ent.text

    # Fecha de nacimiento: Buscar después de "nacido el"
    nacido_index = texto.find("nacido el")
    if nacido_index != -1:
        # Buscar el índice del año (4 dígitos) después de "nacido el"
        año_match = re.search(r'\d{4}', texto[nacido_index:])
        if año_match:
            año_index = año_match.start()
            fecha_nacimiento = texto[nacido_index + len("nacido el") + 1:nacido_index + año_index + 4]
            try:
                date_obj = datetime.strptime(fecha_nacimiento, "%d de %B de %Y")
                fecha_nacimiento = date_obj.strftime("%d/%m/%Y")
            except ValueError as e:
                print("Error al convertir fecha de nacimiento:", e)

    # REGEX para correo y teléfono
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    telefono_regex = r'\b\d{9}\b'

    correo_matches = re.findall(email_regex, texto)
    telefono_matches = re.findall(telefono_regex, texto)

    if correo_matches:
        correo = correo_matches[0]
    if telefono_matches:
        telefono = telefono_matches[0]

    # Diagnostico
    diagnostico_pattern = r'diagn[oó]stico de (.*?)(?=\.)'
    diagnostico_matches = re.findall(diagnostico_pattern, texto)
    if diagnostico_matches:
        diagnostico = diagnostico_matches[0]

    # Próxima cita o revisión
    proxima_cita_pattern = r'(próxima cita|próxima revisión) será el (\d{1,2} de [a-zA-Z]+ de \d{4})'
    proxima_cita_matches = re.findall(proxima_cita_pattern, texto)
    if proxima_cita_matches:
        proxima_cita = proxima_cita_matches[0][1]
        try:
            date_obj = datetime.strptime(proxima_cita, "%d de %B de %Y")
            proxima_cita = date_obj.strftime("%d/%m/%Y")
        except ValueError as e:
            print("Error al convertir próxima cita", e)

    # Exportar a JSON
    datos = {
        "nombre": nombre,
        "fecha_nacimiento": fecha_nacimiento,
        "correo": correo,
        "telefono": telefono,
        "diagnostico": diagnostico,
        "proxima_cita": proxima_cita
    }

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    with open(ruta_salida, "w") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    print("Datos exportados correctamente a", ruta_salida)
