import sys
import configparser
from time import sleep

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox, QDesktopWidget, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal, Qt

from src.bot import IniciarWhatsapp

class whatsapp_web_thread(QThread):
	# Señal para indicar que la tarea ha terminado
	finished = pyqtSignal()
	buscar_msjes = True

	def run(self):
		iniciar_bot = IniciarWhatsapp()
		if iniciar_bot.pantalla_inicio:
			self.buscar_msjes = False

		# Código que se ejecutará en un hilo separado
		while self.buscar_msjes:
			sleep(2)
			iniciar_bot.buscar_nuevo_mensaje()

		# Enviar señal cuando la tarea haya terminado
		self.finished.emit()


class iniciar_ui(QMainWindow):
	#app = QApplication([])
	#Variables de entorno
	config = configparser.ConfigParser()
	config.read('config/env.ini')
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


	def __init__(self):
		super().__init__()
		# UI Qt Designer
		self.ui_ppal = uic.loadUi("ui/principal.ui", self)
		# ui_config = uic.loadUi("ui/config.ui", self)
		# ui_config_selenium = uic.loadUi("ui/config_selenium.ui", self)
		# ui_config_chrome = uic.loadUi("ui/config_chrome.ui", self)

		#Elementos ui principal
		self.btn_iniciar = self.ui_ppal.iniciarBtn
		self.btn_parar = self.ui_ppal.pararBtn
		self.btn_config = self.ui_ppal.configBtn
		self.btn_minimizar = self.ui_ppal.minimizarBtn
		self.btn_salir = self.ui_ppal.salirBtn

		#Elementos ui de configuración
		# self.btn_selenium = ui_config.seleniumBtn
		# self.btn_chrome = ui_config.chromeBtn
		# self.in_t_espera = ui_config.tEsperaInput
		# self.btn_saveConfig0 = ui_config.saveConfigBtn
		# self.btn_volver0 = ui_config.volverBtn 
		# self.btn_reset0 = ui_config.resetBtn
		# self.btn_minimizar0 = ui_config.minimizarBtn
		# self.btn_salir0 = ui_config.salirBtn

		#Elementos ui de configuración - Selenium
		# self.lb_className1 = ui_config_selenium.className1Lb
		# self.lb_className2 = ui_config_selenium.className2Lb
		# self.lb_xPath1 = ui_config_selenium.xPath1Lb
		# self.lb_xPath2 = ui_config_selenium.xPath2Lb
		# self.btn_saveConfig1 = ui_config_selenium.saveConfigBtn
		# self.btn_volver1 = ui_config_selenium.volverBtn
		# self.btn_reset1 = ui_config_selenium.resetBtn
		# self.btn_minimizar1 = ui_config_selenium.minimizarBtn
		# self.btn_salir1 = ui_config_selenium.salirBtn

		#Elementos ui de configuración - Chrome
		# self.in_linux = ui_config_chrome.linuxInput
		# self.in_mac = ui_config_chrome.macInput
		# self.in_windows = ui_config_chrome.windowsInput
		# self.btn_saveConfig2 = ui_config_chrome.saveConfigBtn
		# self.btn_volver2 = ui_config_chrome.volverBtn
		# self.btn_reset2 = ui_config_chrome.resetBtn
		# self.btn_minimizar2 = ui_config_chrome.minimizarBtn
		# self.btn_salir2 = ui_config_chrome.salirBtn

		#Personalizar el marco de las ventanas para que solo muestre un título
		self.ui_ppal.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
		# self.ui_config.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
		# self.ui_config_selenium.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
		# self.ui_config_chrome.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

		#Controladores ui principal
		self.btn_iniciar.clicked.connect(self.iniciar_function)
		self.btn_parar.clicked.connect(self.parar_hilo_function)
		self.btn_config.clicked.connect(self.config_function)
		self.btn_minimizar.clicked.connect(self.ui_ppal.showMinimized)
		self.btn_salir.clicked.connect(self.salir_function)

		#Controladores ui de configuración
		# self.btn_selenium.clicked.connect(self.selenium_function)
		# self.btn_chrome.clicked.connect(self.chrome_function)
		# self.btn_saveConfig0.clicked.connect(self.saveConfig0_function)
		# self.btn_volver0.clicked.connect(self.volver0_function)
		# self.btn_reset0.clicked.connect(self.set_config_param)
		# self.btn_minimizar0.clicked.connect(self.ui_config.showMinimized)
		# self.btn_salir0.clicked.connect(self.salir_function)

		#Controladores ui de configuración - Selenium
		# self.btn_saveConfig1.clicked.connect(self.saveConfig1_function)
		# self.btn_volver1.clicked.connect(self.volver1_function)
		# self.btn_reset1.clicked.connect(self.set_selenium_config)
		# self.btn_minimizar1.clicked.connect(self.ui_config_selenium.showMinimized)
		# self.btn_salir1.clicked.connect(self.salir_function)

		#Controladores ui de configuración - Chrome
		# self.btn_saveConfig2.clicked.connect(self.saveConfig2_function)
		# self.btn_volver2.clicked.connect(self.volver2_function)
		# self.btn_reset2.clicked.connect(self.set_chrome_config)
		# self.btn_minimizar2.clicked.connect(self.ui_config_chrome.showMinimized)
		# self.btn_salir2.clicked.connect(self.salir_function)

		#Iniciar con el botón "PARAR" deshabilitado
		self.btn_parar.setEnabled(False)


	#Funciones Generales
	def salir_function(self):
		self.btn_salir.setEnabled(False)
		try:
			# Enviar la señal para detener el hilo
			self.thread.buscar_msjes = False
			self.thread.wait()
			print("Thread cerrado correctamente")
		except:
			print("No hay Threads abiertos")
		print("Finalizando")
		sys.exit()

	def handle_finished(self):
		# Manejar señal de terminación del hilo
		print("Tarea terminada")
		self.btn_parar.setEnabled(False)
		self.btn_iniciar.setEnabled(True)

	
	#Funciones UI Principal
	def iniciar_function(self):
		print("Iniciando")
		self.btn_iniciar.setEnabled(False)
		self.btn_parar.setEnabled(True)
		# Lanzando hilo Chrome - WhatsApp Web
		self.thread = whatsapp_web_thread()
		self.thread.finished.connect(self.handle_finished)
		self.thread.start()

	def parar_hilo_function(self):
		print("Finalizar hilo")
		self.thread.buscar_msjes = False

	def config_function(self):
		print("Configuración")
		self.pos_ventana = self.ui_ppal.pos()
		self.ui_ppal.hide()
		self.ui_config.move(self.pos_ventana)
		self.set_config_param()
		self.ui_config.show()


	#Funciones UI Configuración
	def set_config_param(self):
		config_dict = dict()
		with open('config/config.txt', 'r') as file:
			for linea in file:
				linea = linea.strip()
				linea_split = linea.split('<e>')
				config_dict[linea_split[0]] = linea_split[1]

		self.in_t_espera.setValue(int(config_dict[self.tiempo_de_espera]))

	def saveConfig0_function(self, s):
		dlg = QMessageBox()
		dlg.setWindowTitle("Guardar cambios")
		dlg.setIcon(QMessageBox.Warning)
		dlg.setText(
			"¿Está seguro de guardar los cambios? "
			"Tenga en cuenta que una vez realizados, "
			"estos cambios no se podrán deshacer. "
			"Por favor, confirme su acción "
			"antes de continuar."
			)
		dlg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		button = dlg.exec()

		if button == QMessageBox.Ok:
			print("Guardando Configuración")
			etiquetas_dict = dict()
			with open('config/config.txt', 'r') as file:
				for linea in file:
					linea = linea.strip()
					linea_split = linea.split('<e>')
					etiquetas_dict[linea_split[0]] = linea_split[1]

			etiquetas_dict[self.tiempo_de_espera]=self.in_t_espera.text()

			with open("config/config.txt", "w") as archivo:
				for clave, valor in etiquetas_dict.items():
					archivo.write(clave + "<e>" + valor + "\n")

	def selenium_function(self):
		print("Configuracion de selenium")
		self.pos_ventana = self.ui_config.pos()
		self.ui_config.hide()
		self.ui_config_selenium.move(self.pos_ventana)
		self.set_selenium_config()
		self.ui_config_selenium.show()

	def chrome_function(self):
		print("Configuracion de chrome")
		self.pos_ventana = self.ui_config.pos()
		self.ui_config.hide()
		self.ui_config_chrome.move(self.pos_ventana)
		self.set_chrome_config()
		self.ui_config_chrome.show()

	def volver0_function(self):
		print("Volver al menú principal")
		self.pos_ventana = self.ui_config.pos()
		self.ui_config.hide()
		self.ui_ppal.move(self.pos_ventana)
		self.ui_ppal.show()


	#Funciones UI Configuración - Selenium
	def set_selenium_config(self):
		config_dict = dict()
		with open('config/config.txt', 'r') as file:
			for linea in file:
				linea = linea.strip()
				linea_split = linea.split('<e>')
				config_dict[linea_split[0]] = linea_split[1]

		self.lb_className1.setText(config_dict[self.class_name1])
		self.lb_className2.setText(config_dict[self.class_name2])
		self.lb_xPath1.setText(config_dict[self.xpath1])
		self.lb_xPath2.setText(config_dict[self.xpath2])

	def saveConfig1_function(self, s):
		dlg = QMessageBox()
		dlg.setWindowTitle("Guardar cambios")
		dlg.setIcon(QMessageBox.Warning)
		dlg.setText(
			"¿Está seguro de guardar los cambios? "
			"Tenga en cuenta que una vez realizados, "
			"estos cambios no se podrán deshacer. "
			"Por favor, confirme su acción "
			"antes de continuar."
			)
		dlg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		button = dlg.exec()

		if button == QMessageBox.Ok:
			print("Guardando Configuración")
			etiquetas_dict = dict()
			with open('config/config.txt', 'r') as file:
				for linea in file:
					linea = linea.strip()
					linea_split = linea.split('<e>')
					etiquetas_dict[linea_split[0]] = linea_split[1]

			etiquetas_dict[self.class_name1]=self.lb_className1.text()
			etiquetas_dict[self.class_name2]=self.lb_className2.text()
			etiquetas_dict[self.xpath1]=self.lb_xPath1.text()
			etiquetas_dict[self.xpath2]=self.lb_xPath2.text()

			with open("config/config.txt", "w") as archivo:
				for clave, valor in etiquetas_dict.items():
					archivo.write(clave + "<e>" + valor + "\n")

	def volver1_function(self):
		print("Volver")
		self.pos_ventana = self.ui_config_selenium.pos()
		self.ui_config_selenium.hide()
		self.ui_config.move(self.pos_ventana)
		self.ui_config.show()


	#Funciones UI Configuración - Chrome
	def set_chrome_config(self):
		config_dict = dict()
		with open('config/config.txt', 'r') as file:
			for linea in file:
				linea = linea.strip()
				linea_split = linea.split('<e>')
				config_dict[linea_split[0]] = linea_split[1]

		self.in_linux.setText(config_dict[self.linux_chrome])
		self.in_mac.setText(config_dict[self.mac_chrome])
		self.in_windows.setText(config_dict[self.windows_chrome])

	def saveConfig2_function(self, s):
		dlg = QMessageBox()
		dlg.setWindowTitle("Guardar cambios")
		dlg.setIcon(QMessageBox.Warning)
		dlg.setText(
			"¿Está seguro de guardar los cambios? "
			"Tenga en cuenta que una vez realizados, "
			"estos cambios no se podrán deshacer. "
			"Por favor, confirme su acción "
			"antes de continuar."
			)
		dlg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		button = dlg.exec()

		if button == QMessageBox.Ok:
			print("Guardando Configuración")
			etiquetas_dict = dict()
			with open('config/config.txt', 'r') as file:
				for linea in file:
					linea = linea.strip()
					linea_split = linea.split('<e>')
					etiquetas_dict[linea_split[0]] = linea_split[1]

			etiquetas_dict[self.linux_chrome]=self.in_linux.text()
			etiquetas_dict[self.mac_chrome]=self.in_mac.text()
			etiquetas_dict[self.windows_chrome]=self.in_windows.text()

			with open("config/config.txt", "w") as archivo:
				for clave, valor in etiquetas_dict.items():
					archivo.write(clave + "<e>" + valor + "\n")

	def volver2_function(self):
		print("Volver")
		self.pos_ventana = self.ui_config_chrome.pos()
		self.ui_config_chrome.hide()
		self.ui_config.move(self.pos_ventana)
		self.ui_config.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = iniciar_ui()
	# Obtener el tamaño de la pantalla
	screen = QDesktopWidget().screenGeometry()
	# Obtener el tamaño de la ventana
	size = window.geometry()
	# Calcular la posición para centrado en la pantalla
	x = int((screen.width() - size.width()) / 2)
	y = int((screen.height() - size.height()) / 2)
	# Mover la ventana a la posición calculada
	window.move(x, y)
	window.show()
	sys.exit(app.exec_())