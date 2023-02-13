import sys
from time import sleep

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal, Qt

from src.bot import IniciarWhatsapp
from src.ui_configurar import Configurar_UI

class Whatsapp_Web_Thread(QThread):
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

class Iniciar_UI(QMainWindow):
	def __init__(self):
		super().__init__()
		# UI Qt Designer
		self.ui_ppal = uic.loadUi("ui/principal.ui", self)
		self.ui_config = Configurar_UI(self.ui_ppal)

		#Personalizar el marco de las ventanas para que solo muestre un título
		self.ui_ppal.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

		#Elementos ui principal
		self.btn_iniciar = self.ui_ppal.iniciarBtn
		self.btn_parar = self.ui_ppal.pararBtn
		self.btn_config = self.ui_ppal.configBtn
		self.btn_minimizar = self.ui_ppal.minimizarBtn
		self.btn_salir = self.ui_ppal.salirBtn

		#Controladores ui principal
		self.btn_iniciar.clicked.connect(self.iniciar_function)
		self.btn_parar.clicked.connect(self.parar_hilo_function)
		self.btn_config.clicked.connect(self.config_function)
		self.btn_minimizar.clicked.connect(self.ui_ppal.showMinimized)
		self.btn_salir.clicked.connect(self.salir_function)

		#Iniciar con el botón "PARAR" deshabilitado
		self.btn_parar.setEnabled(False)


	#Función Salir
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

	# Manejar señal de terminación del hilo
	def handle_finished(self):
		print("Tarea terminada")
		self.btn_parar.setEnabled(False)
		self.btn_iniciar.setEnabled(True)
	
	#Funciones UI Principal
	def iniciar_function(self):
		print("Iniciando")
		self.btn_iniciar.setEnabled(False)
		self.btn_parar.setEnabled(True)
		# Lanzando hilo Chrome - WhatsApp Web
		self.thread = Whatsapp_Web_Thread()
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
		self.ui_config.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Iniciar_UI()
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