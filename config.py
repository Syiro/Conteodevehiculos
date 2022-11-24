import asyncio
import json

import requests
import uvicorn

from app import Conexion, main, models, schemas
from untitled import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QFileDialog


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        #text edit implment
        
        # comobo BOx implement

        self.comboBox.activated.connect(self.modo)
        self.comboBox_4.activated.connect(self.red)

        # horizonslider implement

        self.horizontalSlider_4.valueChanged.connect(self.brillo)
        self.horizontalSlider_5.valueChanged.connect(self.contraste)
        self.horizontalSlider_6.valueChanged.connect(self.color)
        # Radio buttonsimplement
        # self.radioButton_2.toggled.connect(self.tiempoReal)
        # self.radioButton_3.toggled.connect(self.archivo)

        # boton guardarimplement
        self.pushButton_4.clicked.connect(self.enviar)
     
    def fileopen(self,type):
        if type =="Video":
            fname = QFileDialog.getOpenFileName(self,"Open File",""," Videos (*.mp4),(*.wav)") 
        elif type =="Imagenes":
            fname = QFileDialog.getOpenFileName(self,"Open File",""," Imagenes (*.jpg),(*.jpeg),(*.png)") 
        elif type =="Tiempo real":
            print("proximamente")
        return fname
    
    def configactual(self,data):
        self.textEdit.setPlainText(data)
        

    def brillo(self):
        global brillo
        slider = self.sender()
        brillo = slider.value()

    def contraste(self):
        global cont
        slider = self.sender()
        cont = slider.value()

    def color(self):
        global color
        slider = self.sender()
        color = slider.value()

    def modo(self):
        global modo
        combobox = self.sender()
        if combobox.currentText() == "Video":
            modo = "Video"
            type = modo
            self.fileopen(type)          
            self.radioButton_3.setChecked(True)
        if combobox.currentText() == "Imagenes":
            modo = "Imagenes"
            type = modo
            self.fileopen(type) 
            self.radioButton_3.setChecked(True)
        if combobox.currentText() == "Video en Tiempo real":
            modo = "Tiempo real"
            type = modo
            self.fileopen(type) 
            self.radioButton_2.setChecked(True)

    def red(self):
        global red
        combobox = self.sender()
        if combobox.currentText() == "Red1":
            red = "Red1"
        if combobox.currentText() == "Red2":
            red = "Red2"
        if combobox.currentText() == "Red3":
            red = "Red3"

    def enviar(self):
        try:
            modo
            red
            brillo
            cont
            color

        except NameError:
            self.textEdit.setPlainText("Modo de ejecucion no definido apropiadamente")
            print("modo no definido")
            self.showdialog()

        else:
            url = 'http://127.0.0.1:8000/configuracion/'
            pyload = {'brillo': brillo, 'contraste': cont,
                      'color': color, 'modo': modo, 'redneuronal': red}
            data=json.dumps(pyload)
            data2=json.dumps(pyload,indent=6,sort_keys=True,separators =(". ", " = "))
            response = requests.post(url, data)
            self.configactual(data2)
            if response.status_code == 200:
                print(response.content)

    def showdialog(self):
        dialog = QDialog(self)
        dialog.show()


class QDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(QDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("!!ERROR!!")
        self.setFixedSize(200, 100)


if __name__ == "__main__":
    gui = QtWidgets.QApplication([])
    window = MainWindow()
    # asyncio.run(uvi())
    window.show()
    gui.exec_()
