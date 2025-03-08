import os
from src.s1_comando_voz_a_texto import grabar_audio, transcribir_audio
from src.s2_procesamiento_texto_mapeo import procesar_texto
from src.s3_creacion_web_app import app, init_db, borrar_datos
from src.s4_rpa import ejecutar_rpa
import time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "data/clave_api.json"


def main():
    # 1. Manejo de audio y trancripción
    data_folder = "data"
    ruta_transcripcion = os.path.join(data_folder, "transcripcion.txt")
    ruta_json = os.path.join(data_folder, "datos_paciente.json")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    archivo_audio = "grabacion.wav"
    archivo_transcripcion = "transcripcion.txt"

    print("La grabación comenzará en 5 segundos:")
    time.sleep(1)
    print("4")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)

    _ = grabar_audio(data_folder, archivo_audio)
    transcribir_audio(data_folder, archivo_audio, data_folder, archivo_transcripcion)

    # 2. Procesamiento de texto
    if not os.path.exists(ruta_transcripcion):
        with open(ruta_transcripcion, "w") as archivo:
            archivo.write("El paciente es Javier Ríos, nacido el 26 de Diciembre de 2003, con diagnóstico de diabetes mellitus tipo 2. Su correo es javier.algo@gmail.com y su teléfono es 123456789. Su próxima revisión será el 27 de Junio de 2026")

    procesar_texto(ruta_transcripcion, ruta_json)

    # 3. Creación de web app
    init_db()
    borrar_datos()
    app.run(debug=True)

    # 4. Ejecución de RPA
    ejecutar_rpa()


if __name__ == "__main__":
    main()
