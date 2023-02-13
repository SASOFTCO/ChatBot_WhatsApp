import configparser

from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5.QtCore import Qt


class Config_Selenium_UI(QMainWindow):
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


    def __init__(self, ui_config):
        super().__init__()
        # UI Qt Designer
        self.ui_config = ui_config
        self.ui_config_selenium = uic.loadUi("ui/config_selenium.ui", self)

        #Personalizar el marco de las ventanas para que solo muestre un título
        self.ui_config_selenium.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        #Elementos ui de configuración - Selenium
        self.lb_className1 = self.ui_config_selenium.className1Lb
        self.lb_className2 = self.ui_config_selenium.className2Lb
        self.lb_xPath1 = self.ui_config_selenium.xPath1Lb
        self.lb_xPath2 = self.ui_config_selenium.xPath2Lb
        self.btn_reset = self.ui_config_selenium.resetBtn
        self.btn_saveConfig = self.ui_config_selenium.saveConfigBtn
        self.btn_volver = self.ui_config_selenium.volverBtn
        self.btn_minimizar = self.ui_config_selenium.minimizarBtn
        self.btn_salir = self.ui_config_selenium.salirBtn

        #Controladores ui de configuración - Selenium
        self.btn_reset.clicked.connect(self.set_selenium_config)
        self.btn_saveConfig.clicked.connect(self.saveConfig_function)
        self.btn_volver.clicked.connect(self.volver_function)
        self.btn_minimizar.clicked.connect(self.ui_config_selenium.showMinimized)
        self.btn_salir.clicked.connect(self.salir_function)

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

            etiquetas_dict[self.class_name1]=self.lb_className1.text()
            etiquetas_dict[self.class_name2]=self.lb_className2.text()
            etiquetas_dict[self.xpath1]=self.lb_xPath1.text()
            etiquetas_dict[self.xpath2]=self.lb_xPath2.text()

            with open("config/config.txt", "w") as archivo:
                for clave, valor in etiquetas_dict.items():
                    archivo.write(clave + "<e>" + valor + "\n")

    def volver_function(self):
        print("Volver")
        self.pos_ventana = self.ui_config_selenium.pos()
        self.ui_config_selenium.hide()
        self.ui_config.move(self.pos_ventana)
        self.ui_config.show()

    def salir_function(self):
        self.ui_config.salir_function()
