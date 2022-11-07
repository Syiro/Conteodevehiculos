from untitled import *
import asyncio
import uvicorn
from app import models,main,schemas,Conexion
import requests
import json

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self) 
        
        #comobo BOx implement 
        
        self.comboBox.activated.connect(self.modo)
        self.comboBox_4.activated.connect(self.red)
        
        #horizonslider implement
        
        self.horizontalSlider_4.valueChanged.connect(self.brillo)
        #Radio buttonsimplement
        #self.radioButton_2.toggled.connect(self.tiempoReal)
        #self.radioButton_3.toggled.connect(self.archivo)
        
        #boton guardarimplement
        self.pushButton_4.clicked.connect(self.enviar)
        
    def brillo(self):
        global brillo
        slider = self.sender()
        brillo = slider.value()
        print(brillo)
        
        
        
    def modo(self):
        global modo
        combobox = self.sender()
        if combobox.currentText()=="Video":
            modo="Video"
            self.radioButton_3.setChecked(True)
        if combobox.currentText()=="Imagenes":
            modo="Imagenes"
            self.radioButton_3.setChecked(True)
        if combobox.currentText()=="Video en Tiempo real":
            modo="Tiempo real"
            self.radioButton_2.setChecked(True)
        
        
    def red(self):
        global red 
        combobox = self.sender()
        if combobox.currentText()=="Red1":
            red="Red1"
        if combobox.currentText()=="Red2":
            red="Red2"
        if combobox.currentText()=="Red3":
            red="Red3"
        
    
            
    # def tiempoReal(self):
    #     radioButton = self.sender()
    #     if radioButton.isChecked():
    #         global modo
    #         modo = "Tiempo real"
            
    # def archivo(self):
    #     radioButton= self.sender()
    #     if radioButton.isChecked():
    #         global modo
    #         modo = "Archivo"
    
    # def video(self):
    #     pass
    
    
        
    
    def enviar(self):
        try:
            modo
            red
        
        except NameError:
            print("modo no definido")
            self.showdialog()

        else:
            
            url = 'http://127.0.0.1:8000/configuracion/'
            pyload = {'brillo':300,'contraste':10,'color':10,'modo':modo,'redneuronal':red}
            response = requests.post(url, data=json.dumps(pyload))
            print(response.url)
            
            if response.status_code==200:
                print(response.content)
    def showdialog(self):
        dialog=Dialog(self)
        dialog.show()
        
class Dialog(QDialog):
    def __init__(self,*args, **kwargs) :
        super(Dialog,self).__init__(*args,**kwargs)
        self.setWindowTitle("!!ERROR!!")
        self.setFixedSize(200,100)
        
    
if __name__ == "__main__":
    gui = QtWidgets.QApplication([])
    window = MainWindow()
    #asyncio.run(uvi())
    window.show()
    gui.exec_()