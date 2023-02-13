import configparser

from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5.QtCore import Qt


class Config_Chrome_UI(QMainWindow):
    #Variables de entorno
    config = configparser.ConfigParser()
    config.read('config/env.ini')
    #Carpeta local de la cache de Chrome 
    linux_chrome = config.get('env2', 'linux_chrome')
    mac_chrome = config.get('env2', 'mac_chrome')
    windows_chrome = config.get('env2', 'windows_chrome')

    def __init__(self, ui_config):
        super().__init__()
        # UI Qt Designer
        self.ui_config = ui_config
        self.ui_config_chrome = uic.loadUi("ui/config_chrome.ui", self)

        #Personalizar el marco de las ventanas para que solo muestre un título
        self.ui_config_chrome.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        
        #Elementos ui de configuración - Chrome
        self.in_linux = self.ui_config_chrome.linuxInput
        self.in_mac = self.ui_config_chrome.macInput
        self.in_windows = self.ui_config_chrome.windowsInput
        self.btn_reset = self.ui_config_chrome.resetBtn
        self.btn_saveConfig = self.ui_config_chrome.saveConfigBtn
        self.btn_volver = self.ui_config_chrome.volverBtn
        self.btn_minimizar = self.ui_config_chrome.minimizarBtn
        self.btn_salir = self.ui_config_chrome.salirBtn

        #Controladores ui de configuración - Chrome
        self.btn_reset.clicked.connect(self.set_chrome_config)
        self.btn_saveConfig.clicked.connect(self.saveConfig_function)
        self.btn_volver.clicked.connect(self.volver_function)
        self.btn_minimizar.clicked.connect(self.ui_config_chrome.showMinimized)
        self.btn_salir.clicked.connect(self.salir_function)


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

    def saveConfig_function(self, s):
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

    def volver_function(self):
        print("Volver")
        self.pos_ventana = self.ui_config_chrome.pos()
        self.ui_config_chrome.hide()
        self.ui_config.move(self.pos_ventana)
        self.ui_config.show()

    def salir_function(self):
        self.ui_config.salir_function()