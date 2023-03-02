import webbrowser

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
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
        self.user_guide_pdf = self.ui_config.userGuide
        self.code_guide = self.ui_config.codeGuide
        self.info_soft = self.ui_config.infoSoft
        self.btn_selenium = self.ui_config.seleniumBtn
        self.btn_chrome = self.ui_config.chromeBtn
        self.btn_tiempos = self.ui_config.tiemposBtn
        self.btn_volver = self.ui_config.volverBtn
        self.btn_minimizar = self.ui_config.minimizarBtn
        self.btn_salir = self.ui_config.salirBtn

        #Controladores ui de configuración
        self.user_guide_pdf.mousePressEvent = self.abrir_manual_usuario
        self.code_guide.mousePressEvent = self.abrir_doc_code
        self.info_soft.mousePressEvent = self.info_soft_function
        self.btn_selenium.clicked.connect(self.selenium_function)
        self.btn_chrome.clicked.connect(self.chrome_function)
        self.btn_tiempos.clicked.connect(self.tiempos_function)
        self.btn_volver.clicked.connect(self.volver_function)
        self.btn_minimizar.clicked.connect(self.ui_config.showMinimized)
        self.btn_salir.clicked.connect(self.salir_function)


	#Funciones UI Configuración
    def abrir_manual_usuario(self, event):
        print("Abrir el manual de usuario")
        filename = "docs/Manual_Usuario.pdf"
        webbrowser.open(filename, new = 2)

    def abrir_doc_code(self, event):
        print("Abrir la documentación del código")
        filename = "docs/Manual_Codigo_Fuente.pdf"
        webbrowser.open(filename, new = 2)

    def info_soft_function(self, event):
        print("Información del sistema")
        dlg = QMessageBox()
        dlg.setWindowTitle("Información Del Sistema")
        dlg.setIcon(QMessageBox.Warning)
        dlg.setText(
            "OpenAI = 0.26.5"
            "\nPython = 3.10.6"
            "\nSelenium = 4.8.0"
            "\nPyQt5 = 5.15.9"
            "\nQT Designer = 5.15.3"
            "\nCrhome = 110.0.5481.77"
            )
        dlg.setStandardButtons(QMessageBox.Ok)
        button = dlg.exec()


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


    # Funciones para leer y guardar las configuraciones en el txt
    def leer_config(self):
        config_dict = dict()
        with open('config/config.txt', 'r') as file:
            for linea in file:
                linea = linea.strip()
                linea_split = linea.split('<e>')
                config_dict[linea_split[0]] = linea_split[1]
        return config_dict

    def guardar_config(self, config_dict):
        with open("config/config.txt", "w") as archivo:
            for clave, valor in config_dict.items():
                archivo.write(clave + "<e>" + valor + "\n")