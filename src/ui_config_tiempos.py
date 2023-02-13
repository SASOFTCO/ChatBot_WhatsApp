import configparser

from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5.QtCore import Qt


class Config_Tiempos_UI(QMainWindow):
    #Variables de entorno
    config = configparser.ConfigParser()
    config.read('config/env.ini')
    #Tiempos de espera
    te_rta_gpt = config.get('env3', 't_e_rta_gpt')
    te_init_whats = config.get('env3', 't_e_init_whats')
    te_msg = config.get('env3', 't_e_msg')

    def __init__(self, ui_config):
        super().__init__()
        # UI Qt Designer
        self.ui_config = ui_config
        self.ui_config_tiempos = uic.loadUi("ui/config_tiempos.ui", self)

        #Personalizar el marco de las ventanas para que solo muestre un título
        self.ui_config_tiempos.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        
        #Elementos ui de configuración - Tiempos
        self.in_rta_gpt = self.ui_config_tiempos.rtaGPTInput
        self.in_init_whats = self.ui_config_tiempos.inicioWhatsappInput
        self.in_msg = self.ui_config_tiempos.msgInput
        self.btn_reset = self.ui_config_tiempos.resetBtn
        self.btn_saveConfig = self.ui_config_tiempos.saveConfigBtn
        self.btn_volver = self.ui_config_tiempos.volverBtn
        self.btn_minimizar = self.ui_config_tiempos.minimizarBtn
        self.btn_salir = self.ui_config_tiempos.salirBtn

        #Controladores ui de configuración - Tiempos
        self.btn_reset.clicked.connect(self.set_tiempos_config)
        self.btn_saveConfig.clicked.connect(self.saveConfig_function)
        self.btn_volver.clicked.connect(self.volver_function)
        self.btn_minimizar.clicked.connect(self.ui_config_tiempos.showMinimized)
        self.btn_salir.clicked.connect(self.salir_function)


    #Funciones UI Configuración - Tiempos
    def set_tiempos_config(self):
        config_dict = dict()
        with open('config/config.txt', 'r') as file:
            for linea in file:
                linea = linea.strip()
                linea_split = linea.split('<e>')
                config_dict[linea_split[0]] = linea_split[1]

        self.in_rta_gpt.setValue(int(config_dict[self.te_rta_gpt]))
        self.in_init_whats.setValue(int(config_dict[self.te_init_whats]))
        self.in_msg.setValue(int(config_dict[self.te_msg]))

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

            etiquetas_dict[self.te_rta_gpt]=self.in_rta_gpt.text()
            etiquetas_dict[self.te_init_whats]=self.in_init_whats.text()
            etiquetas_dict[self.te_msg]=self.in_msg.text()

            with open("config/config.txt", "w") as archivo:
                for clave, valor in etiquetas_dict.items():
                    archivo.write(clave + "<e>" + valor + "\n")

    def volver_function(self):
        print("Volver")
        self.pos_ventana = self.ui_config_tiempos.pos()
        self.ui_config_tiempos.hide()
        self.ui_config.move(self.pos_ventana)
        self.ui_config.show()

    def salir_function(self):
        self.ui_config.salir_function()