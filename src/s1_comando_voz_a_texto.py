import pyaudio
import wave
from google.cloud import speech
import io
import os
import time


def grabar_audio(output_folder, archivo_audio="grabacion.wav", tasa_muestreo=16000, duracion=30, silencio_max=3) -> str:
    '''
    Graba audio mediante el micrófono del dispositivo y lo guarda en un archivo WAV.

    Returns:
    str: Ruta del archivo de audio grabado
    '''
    formato = pyaudio.paInt16
    canales = 1  # Mono
    buffer = 1024
    umbral_silencio = 500

    ruta_audio = os.path.join(output_folder, archivo_audio)

    p = pyaudio.PyAudio()
    print("Grabando...")

    stream = p.open(format=formato,
                    channels=canales,
                    rate=tasa_muestreo,
                    input=True,
                    frames_per_buffer=buffer)

    frames = []
    tiempo_silencio = 0
    tiempo_inicio = time.time()
    
    while True:
        data = stream.read(buffer)
        frames.append(data)

        nivel_volumen = max(abs(int.from_bytes(data[i:i+2], byteorder='little', signed=True)) for i in range(0, len(data), 2))

        # Verificar si hay silencio
        if nivel_volumen < umbral_silencio:
            tiempo_silencio += buffer / tasa_muestreo
        else:
            tiempo_silencio = 0

        # Detener grabación si se supera el tiempo de duración o si hay silencio por más de 3 segundos
        if tiempo_silencio >= silencio_max or (time.time() - tiempo_inicio) >= duracion:
            break

    print("Fin de la grabación")

    stream.stop_stream()
    stream.close()

    with wave.open(ruta_audio, 'wb') as wf:
        wf.setnchannels(canales)
        wf.setsampwidth(p.get_sample_size(formato))
        wf.setframerate(tasa_muestreo)
        wf.writeframes(b''.join(frames))

    p.terminate()
    print("Audio guardado en {}".format(ruta_audio))
    return ruta_audio


def transcribir_audio(input_folder, archivo_audio="grabacion.wav", output_folder=None, output_file="transcripcion.txt") -> str:
    '''
    Transcribe un archivo de audio a texto mediante la API de Google Cloud Speech-to-Text.

    Returns:
    str: Ruta del archivo de texto con la transcripción
    '''
    print("Transcribiendo audio...")
    cliente = speech.SpeechClient()

    ruta_audio = os.path.join(input_folder, archivo_audio)
    if not output_folder:
        output_folder = input_folder
    ruta_transcripcion = os.path.join(output_folder, output_file)

    with io.open(ruta_audio, "rb") as archivo_audio:
        contenido = archivo_audio.read()

    audio = speech.RecognitionAudio(content=contenido)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="es-ES",
    )

    respuesta = cliente.recognize(config=config, audio=audio)

    # Exportar a txt
    with open(ruta_transcripcion, "w") as archivo:
        for resultado in respuesta.results:
            archivo.write(resultado.alternatives[0].transcript)
            print("Transcripción: {}".format(resultado.alternatives[0].transcript))

    print("Transcripción guardada en {}".format(ruta_transcripcion))
    return ruta_transcripcion

# if __name__ == "__main__":
#     grabar_audio()
#     transcribir_audio("grabacion.wav")
