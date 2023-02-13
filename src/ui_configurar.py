from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt

from src.ui_config_selenium import Config_Selenium_UI
from src.ui_config_chrome import Config_Chrome_UI
from src.ui_config_tiempos import Config_Tiempos_UI


class Configurar_UI(QMainWindow):
    def __init__(self, ui_ppal):
        super().__init__()
        # UI Qt Designer
        self.ui_ppal = ui_ppal
        self.ui_config = uic.loadUi("ui/config.ui", self)
        self.ui_config_selenium = Config_Selenium_UI(self.ui_config)
        self.ui_config_chrome = Config_Chrome_UI(self.ui_config)
        self.ui_config_tiempos = Config_Tiempos_UI(self.ui_config)

        #Personalizar el marco de las ventanas para que solo muestre un título
        self.ui_config.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        #Elementos ui de configuración
        self.btn_selenium = self.ui_config.seleniumBtn
        self.btn_chrome = self.ui_config.chromeBtn
        self.btn_tiempos = self.ui_config.tiemposBtn
        self.btn_volver = self.ui_config.volverBtn
        self.btn_minimizar = self.ui_config.minimizarBtn
        self.btn_salir = self.ui_config.salirBtn

        #Controladores ui de configuración
        self.btn_selenium.clicked.connect(self.selenium_function)
        self.btn_chrome.clicked.connect(self.chrome_function)
        self.btn_tiempos.clicked.connect(self.tiempos_function)
        self.btn_volver.clicked.connect(self.volver_function)
        self.btn_minimizar.clicked.connect(self.ui_config.showMinimized)
        self.btn_salir.clicked.connect(self.salir_function)


	#Funciones UI Configuración
    def selenium_function(self):
        print("Configuracion de selenium")
        self.pos_ventana = self.ui_config.pos()
        self.ui_config.hide()
        self.ui_config_selenium.move(self.pos_ventana)
        self.ui_config_selenium.set_selenium_config()
        self.ui_config_selenium.show()

    def chrome_function(self):
        print("Configuracion de chrome")
        self.pos_ventana = self.ui_config.pos()
        self.ui_config.hide()
        self.ui_config_chrome.move(self.pos_ventana)
        self.ui_config_chrome.set_chrome_config()
        self.ui_config_chrome.show()

    def tiempos_function(self):
        print("Configuración tiempos de espera")
        self.pos_ventana = self.ui_config.pos()
        self.ui_config.hide()
        self.ui_config_tiempos.move(self.pos_ventana)
        self.ui_config_tiempos.set_tiempos_config()
        self.ui_config_tiempos.show()

    def volver_function(self):
        print("Volver al menú principal")
        self.pos_ventana = self.ui_config.pos()
        self.ui_config.hide()
        self.ui_ppal.move(self.pos_ventana)
        self.ui_ppal.show()

    def salir_function(self):
        self.ui_ppal.salir_function()
