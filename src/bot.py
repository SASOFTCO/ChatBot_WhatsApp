import openai
import threading
import configparser
import platform
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

class IniciarWhatsapp:
    #Variable para retorna la respuesta de GPT-3
    rta_gpt = ""

    #Leer API Key ChatGPT
    config = configparser.ConfigParser()
    config.read('config/env.ini')
    api_key = config.get('login', 'api_key')
    openai.api_key = api_key

    #Variables de entorno
    #class_name1 = msjes_nuevos_class_name (Clase para identificar mensajes nuevos)
    class_name1 = config.get('env1', 'class_name1')
    #class_name2 = conversacion_class_name (Clase para identificar los mensajes de la conversación actual)
    class_name2 = config.get('env1', 'class_name2')
    #xpath1 = input_box_path (xpath para identificar el input box - caja de respuesta)
    xpath1 = config.get('env1', 'xpath1')
    #xpath2 = not_spam_btn_path (xpath para identificar el botón OK de una conversación nueva)
    xpath2 = config.get('env1', 'xpath2')
    #Carpeta local de la cache de Chrome 
    linux_chrome = config.get('env2', 'linux_chrome')
    mac_chrome = config.get('env2', 'mac_chrome')
    windows_chrome = config.get('env2', 'windows_chrome')
    #Tiempo de espera para la respuesta de GPT-3
    tiempo_de_espera = config.get('env2', 'tiempo_espera')

    #Leer e iniciar las etiquetas de whatsapp web guardadas en el txt
    config_dict = dict()
    with open('config/config.txt', 'r') as file:
        for linea in file:
            linea = linea.strip()
            linea_split = linea.split('<e>')
            config_dict[linea_split[0]] = linea_split[1]

    msjes_nuevos_class_name = config_dict[class_name1]
    conversacion_class_name = config_dict[class_name2]
    input_box_path = config_dict[xpath1]
    not_spam_btn_path = config_dict[xpath2]

    linux_cache = config_dict[linux_chrome]
    mac_cache = config_dict[mac_chrome]
    windows_cache = config_dict[windows_chrome]

    tiempo_espera = config_dict[tiempo_de_espera]

    def __init__(self):
        #Abrir WhatsApp
        sistema_operativo = platform.system()
        options=webdriver.ChromeOptions()
        #options.add_experimental_option("excludeSwitches", ["enable-logging"])
        print("Abrir WhatsApp")
        if sistema_operativo == "Linux":
            try:
                options.add_argument(f'user-data-dir={self.linux_cache}')
                self.driver=webdriver.Chrome(executable_path="bin/linux/chromedriver", chrome_options=options)
                print("Linux cache load")
            except:
                options=webdriver.ChromeOptions()
                self.driver=webdriver.Chrome(executable_path="bin/linux/chromedriver", chrome_options=options)
                print("Linux sin browser_cache_path definida.")
        elif sistema_operativo == "Darwin":
            try:
                options.add_argument(f'user-data-dir={self.mac_cache}')
                self.driver=webdriver.Chrome(executable_path="bin/mac/chromedriver.exe", chrome_options=options)
                print("Mac cache load")
            except:
                options=webdriver.ChromeOptions()
                self.driver=webdriver.Chrome(executable_path="bin/mac/chromedriver.exe", chrome_options=options)
                print("Mac sin browser_cache_path definida.")
        elif sistema_operativo == "Windows":
            try:
                options.add_argument(f'user-data-dir={self.windows_cache}')
                self.driver=webdriver.Chrome(executable_path="bin/windows/chromedriver.exe", chrome_options=options)
                print("Windows cache load")
            except:
                options=webdriver.ChromeOptions()
                print("Windows sin browser_cache_path definida.")
                self.driver=webdriver.Chrome(executable_path="bin/windows/chromedriver.exe", chrome_options=options)

        
        self.driver.get("https://web.whatsapp.com/")
        self.wait=WebDriverWait(self.driver,100)
        self.wait2=WebDriverWait(self.driver,1)

        #Esperar que carguen los mensajes y hacer clkic en el primero
        mensajes_nuevos = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, self.msjes_nuevos_class_name)))
        mensajes_nuevos[0].click()
        sleep(.5)
        

    def obtener_respuesta(self, mensaje):
        mensaje+= '. Responda en pocas palabras y en un único parrágrafo.'
        #mensaje+= '. Sea claro, conciso, directo y responda en un solo párrafo.'
        try:
            completions = openai.Completion.create(
                engine="text-davinci-003",
                prompt=mensaje,
                max_tokens=1024,
                temperature=0.9,
                n=1,
                stop=None,
            )
            respuesta = completions.choices[0].text
            self.rta_gpt = respuesta.strip()
        except openai.error.ServiceUnavailableError as e:
            # respuesta = 'Lo sentimos, pero en este momento el servicio no se encuentra disponible.'
            self.rta_gpt = 'Lo sentimos, pero en este momento el servicio no se encuentra disponible.'
        except:
            # respuesta = 'Lo sentimos, en este momento estamos experimentando dificultades técnicas.'
            self.rta_gpt = 'Lo sentimos, en este momento estamos experimentando dificultades técnicas.'
        #return respuesta.strip()

    #Conexión con Chat GPT
    def respuesta_chatgpt(self, mensaje):
        hilo = threading.Thread(target=self.obtener_respuesta, args=(mensaje,))
        hilo.start()
        hilo.join(timeout=self.tiempo_espera)
        if hilo.is_alive():
            respuesta = 'Lo sentimos, no se pudo obtener una respuesta en el tiempo establecido.'
        else:
            # respuesta = self.obtener_respuesta(mensaje)
            respuesta = self.rta_gpt
        return respuesta
        


    #Obtener el mensaje, consultarlo en chatgpt y retornar la respuesta a la conversación
    def procesar_mensaje(self):
        #Acción para dar click en el botón "OK" de una conversación nueva
        try:
            not_spam_btn = self.wait2.until(EC.presence_of_element_located((By.XPATH,self.not_spam_btn_path)))
            not_spam_btn.click()
            sleep(.5)
            print("Nueva conversación")
        except:
            print("Conversación existente")

        # Esperar a que se carguen los mensajes
        conversacion = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, self.conversacion_class_name)))
        # Obtener el último mensaje de la conversación
        msj_actual = conversacion[-1].text
        # Utilizando splitlines() para eliminar la hora del mensaje
        msj_actual = msj_actual.splitlines()[:-1]
        msj_actual = "\n".join(msj_actual)
        print(f"Mensaje actual: {msj_actual}")
        
        #Respuesta de Chat GPT
        rta_chatgpt = self.respuesta_chatgpt(msj_actual)
        print(f"Esta es la respuesta devuelta de chatGPT: {rta_chatgpt}")
        
        #Enviar respuesta
        input_box = self.wait2.until(EC.presence_of_element_located((By.XPATH,self.input_box_path)))
        input_box.send_keys(rta_chatgpt)
        input_box.send_keys(Keys.RETURN)
        mensajes_nuevos = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, self.msjes_nuevos_class_name)))
        mensajes_nuevos[0].click()


    #Buscar nuevos mensajes
    def buscar_nuevo_mensaje(self):
        mensajes_nuevos = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, self.msjes_nuevos_class_name)))
        
        if len(mensajes_nuevos) > 1:
            mensajes_nuevos.pop(0)
            for mensaje in mensajes_nuevos:
                #print(f"Mensajes no leidos de esta conversación: {mensaje.text}")
                mensaje.click()
                sleep(1)
                self.procesar_mensaje()

        else:
            mensajes_nuevos[0].click()
            print('No hay mensajes nuevos')
