from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import os


PATH_TO_DRIVER = os.path.join("drivers", "chromedriver.exe")


def prueba_navegador():
    service = Service(PATH_TO_DRIVER)
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.google.com")
    print(driver.title)
    driver.quit()


# Cargar datos procesados
def cargar_datos():
    path_to_json = os.path.join("data", "datos_paciente.json")
    with open(path_to_json, "r") as archivo:
        datos = json.load(archivo)
    return datos


# RPA para rellenar formulario
def rellenar_formulario(datos):
    # Inicializar navegador
    service = Service(PATH_TO_DRIVER)
    driver = webdriver.Chrome(service=service)
    driver.get("http://127.0.0.1:5000/")

    # Rellenar formulario
    try:
        driver.find_element(By.NAME, "nombre").send_keys(datos["nombre"])
        driver.find_element(By.NAME, "fecha_nacimiento").send_keys(datos["fecha_nacimiento"])
        driver.find_element(By.NAME, "email").send_keys(datos["correo"])
        driver.find_element(By.NAME, "telefono").send_keys(datos["telefono"])
        driver.find_element(By.NAME, "diagnostico").send_keys(datos["diagnostico"])
        driver.find_element(By.NAME, "fecha_revision").send_keys(datos["proxima_cita"])

        # Enviar formulario
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        print("Formulario enviado correctamente")
    except Exception as e:
        print("Error al rellenar formulario", e)
    finally:
        time.sleep(2)
        driver.quit()


def ejecutar_rpa():
    '''
    Carga los datos del paciente y rellena el formulario de la web app
    '''
    datos = cargar_datos()
    rellenar_formulario(datos)
