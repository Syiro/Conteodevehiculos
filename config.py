import asyncio
import json
import sys
import requests
import uvicorn
from configcolor import*
from ejecucion import Ejecucion
from app import Conexion, main, models, schemas
from untitled import *
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QPushButton, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow,ConfigColor,Ejecucion):
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
        

        # boton guardarimplement
        self.pushButton_4.clicked.connect(self.enviar)
        
        # boton importarimplement
        self.pushButton_3.clicked.connect(self.importar)
        
        # radio button automaticoimplement
        self.radioButton.toggled.connect(self.automatico)

        # start button implement
        self.pushButton_12.clicked.connect(self.modoejecucion)
        
    def modoejecucion(self):
        self.Ejecucion_mode(modo=modo,red=red)
        self.Mostrar_img(fname=fname,brillo=brillo,color=color,cont=cont)
        self.Inferencia(img=fname)
        
    def automatico(self):
        brillo=10
        color=10
        cont=10
        self.label_18.setPixmap(QPixmap(self.configuracionbrillo(fname,brillo)))
        self.label_18.setPixmap(QPixmap(self.configuracioncolor(fname,color)))
        self.label_18.setPixmap(QPixmap(self.configuracioncontraste(fname,cont)))
        self.horizontalSlider_4.setValue(brillo)
        self.horizontalSlider_5.setValue(cont)
        self.horizontalSlider_6.setValue(color)
        
        
    def importar(self):
        url = 'http://127.0.0.1:8000/configuracion/'
        data,b = QFileDialog.getOpenFileName(self,'Open File',''," Json (*.json)") 
        file = open(data)
        data = json.load(file)
        response = requests.post(url, data)
        data2=json.dumps(data,indent=6,sort_keys=True,separators =(". ", " = "))
        self.configactual(data2)
        self.enviarimport(data)
        if response.status_code == 200:
            print(response.content)
    
    def enviarimport(self,data):
        global brillo,cont,color,modo,red
        brillo = data["brillo"]
        cont = data["contraste"]
        color = data["color"]
        modo = data["modo"]
        red = data["redneuronal"]
        self.horizontalSlider_4.setValue(brillo)
        self.horizontalSlider_5.setValue(cont)
        self.horizontalSlider_6.setValue(color)
       
        index=self.comboBox.findText(modo)
        index2=self.comboBox_4.findText(red)
        self.comboBox.setCurrentIndex(index)
        self.comboBox_4.setCurrentIndex(index2)
        
        if fname!="" and brillo!=10 and cont !=10:
            self.label_18.setPixmap(QPixmap(self.configuracionbrillo(fname,color)))
        elif fname!="" and brillo!=10 and color !=10:
            self.label_18.setPixmap(QPixmap(self.configuracionbrillo(fname,cont)))
        elif fname!="" and cont!=10 and color !=10:
            self.label_18.setPixmap(QPixmap(self.configuracionbrillo(fname,brillo)))
            
        
    
    def configuracionbrillo(self,path,brillo):
        pathout = self.configbrillo(path=path,brillo=brillo)
        return pathout
    
    def configuracioncontraste(self,path,cont):
        pathout = self.configcontraste(path=path,contraste=cont)
        return pathout
    
    def configuracioncolor(self,path,color):
        pathout = self.configcolor(path=path,color=color)
        return pathout
        
      
    
    def fileopen(self,type):
        global fname
        if type =="Video":
            fname = QFileDialog.getOpenFileName(self,"Open File",""," Videos (*.mp4 *.wav)") 
        elif type =="Imagenes":
            fname,b = QFileDialog.getOpenFileName(self,'Open File',''," Imagenes (*.jpg *.jpeg *.png)") 
            self.label_18.setPixmap(QPixmap(fname))
            
        elif type =="Tiempo real":
            print("proximamente")
            fname=""
        
       
    
    def filesave(self,data):
        sname,b = QFileDialog.getSaveFileName(self,'Save file','',"Json (*.json)")
        file = open(sname,'w')
        file.write(data)
        file.close()
    
       
        
        
    def configactual(self,data):
        self.textEdit.setPlainText(data)
        
    # def modyfiimage(self):
    #     global brillo,cont,color
    #     brillo = self.horizontalSlider_4.value()
    #     cont = self.horizontalSlider_5.value()
    #     color = self.horizontalSlider_6.value()
    #     self.label_18.setPixmap(QPixmap(self.convertimage(fname,brillo,cont,color)))
    
    def brillo(self):
        global brillo,cont,color
        cont=10
        color=10
        self.horizontalSlider_5.setValue(cont)
        self.horizontalSlider_6.setValue(color)
        self.radioButton.setChecked(False)
        slider = self.sender()
        brillo = slider.value()
        self.label_18.setPixmap(QPixmap(self.configuracionbrillo(fname,brillo)))
        
        
    def contraste(self):
        global brillo,cont,color
        brillo=10
        color=10
        self.horizontalSlider_4.setValue(brillo)
        self.horizontalSlider_6.setValue(color)
        self.radioButton.setChecked(False)
        slider = self.sender()
        cont = slider.value()
        self.label_18.setPixmap(QPixmap(self.configuracioncontraste(fname,cont)))
        
    
    def color(self):
        global brillo,cont,color
        brillo=10
        cont=10
        self.horizontalSlider_4.setValue(brillo)
        self.horizontalSlider_5.setValue(cont)
        self.radioButton.setChecked(False) 
        slider = self.sender()
        color = slider.value()
        self.label_18.setPixmap(QPixmap(self.configuracioncolor(fname,color)))
        
        
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
        return modo

    def red(self):
        global red
        combobox = self.sender()
        if combobox.currentText() == "SSD Movilnet 2.0 fpnlite":
            red = "SSD Movilnet 2.0 fpnlite"
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
            self.showdialog()

        else:
            url = 'http://127.0.0.1:8000/configuracion/'
            pyload = {'brillo': brillo, 'contraste': cont,
                      'color': color, 'modo': modo, 'redneuronal': red}
            data=json.dumps(pyload)
            data2=json.dumps(pyload,indent=6,sort_keys=True,separators =(". ", " = "))
            response = requests.post(url, data)
            self.configactual(data2)
            self.filesave(data)
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