import asyncio
import json
import sys
import os
import requests
import uvicorn
from enviar import*
from configcolor import*
from ejecucion import *
from dialogos import*
from videoplayer import*
from videothread import *
import pafy
sys.path.insert(0, '/home/ruben-laptop/Tesis/code/')
from  app import Conexion, main, models, schemas
from untitled import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import numpy as np
from imutils.video import FPS

#export QT_QPA_PLATFORM=xcb
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["QT_QPA_PLATFORM"] = "xcb"
#os.environ["PAFY_BACKEND"] = "internal"
#to open designer on venv qt5-tools designer
#video test https://www.youtube.com/watch?v=APpB5Agw8d4&ab_channel=PrakharSachan

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs) 
        #objetos:
        
        #conectar con el url Dialog
        self.url_dialog = URLDialog(self) # instancia de la clase URLDialog
        # Conectar la señal urlEntered de URLDialog al método on_url_entered de MainWindow
        self.url_dialog.urlEntered.connect(self.on_url_entered)
        
        #conectar con hilo de deteccion 
        self.videodetec = VideoAnalyzer(video_path="")
        self.videodetec.videoEntered.connect(self.on_video_entered)
        
        
        self.thread = VideoThread(fname="",tiemporeal=False)
        
        
        self.setupUi(self)
        # comobo BOx implement
        self.comboBox.activated.connect(self.modo)
       # self.comboBox_4.activated.connect(self.red
        # horizonslider implement
        self.horizontalSlider_4.valueChanged.connect(self.brillo)
        self.horizontalSlider_5.valueChanged.connect(self.contraste)
        self.horizontalSlider_6.valueChanged.connect(self.color)
        # boton guardarimplement
        self.pushButton_4.clicked.connect(self.send)
        # boton importarimplement
        self.pushButton_3.clicked.connect(self.importar)
        # radio button automaticoimplement
        self.radioButton.toggled.connect(self.automatico)
        # start button implement
        self.pushButton_12.clicked.connect(self.modoejecucion)
        # stop button implement
        self.pushButton_13.clicked.connect(self.closeEvent)
        #selec rd implement
        self.pushButton.clicked.connect(self.abrirred)
        #guardar button implement
        self.pushButton_2.clicked.connect(self.guardar)
        self.pushButton_6.clicked.connect(self.auto)
       # self.pushButton_7.clicked.connect(self.reseteo)
       
    @pyqtSlot(np.ndarray)  
    def on_video_entered(self,frame):
        qt_img = self.convert_cv_qt(frame)
        self.label_26.setPixmap(qt_img)

        
    @pyqtSlot(int) 
    def on_count_entered(self,totalUp):
        count = totalUp
        self.label_25.setText(str(count))
        
          
    def send(self):
        try:
            modo
            red
            brillo
            cont
            color 
            treshold
            
        except NameError: 
            self.textEdit.setPlainText("Modo de ejecucion no definido apropiadamente")
            self.showdialog()
        else:
            
            if modo == "Video" or modo=="Video en Tiempo real":
                Enviar.enviar(self=self,modo=modo, red=red, brillo = 1,
                                cont=1, color=1, treshold=treshold, skipfps=skipfps)
            else:
                Enviar.enviar(self=self,modo=modo, red=red, brillo = brillo,
                                cont=cont, color=color, treshold=treshold, skipfps=0)

            
    def handle_detection(self, detected):
            if detected:
                print("Vehículo detectado")
                
    def auto(self):
        global color, cont, brillo ,red ,skipfps , treshold
        color=10
        cont=10
        brillo=10
        skipfps=30
        treshold=0.3
        pathname = "fine_tuned_model.zip"
        red = pathname
        self.lineEdit.setText(skipfps)
        self.lineEdit_2.setText(treshold)
        self.horizontalSlider_4.setValue(brillo)
        self.horizontalSlider_5.setValue(cont)
        self.horizontalSlider_6.setValue(color)
        Ejecucion.Cargaparametros(self,pathmodel=pathname)
        self.label_28.setText(pathname)
        if modo == "Imagenes" :
            self.send()
        elif modo == "Video":
            self.send()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        global b
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        if b != 1: #condicion videos cargados para vizualizar en config
            self.label_18.setPixmap(qt_img)
            
        else  : #condicion videos cargados para ejecucion
            self.label_26.setPixmap(qt_img) 
            

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        Image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        convertir_QT = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
        pic = convertir_QT.scaled(800, 600, Qt.KeepAspectRatio)
        return QPixmap.fromImage(pic)

    def closeEvent(self, event):
        self.thread.stop()
        self.label_26.clear()
        event.accept()

    def guardar(self):
        global skipfps, treshold
        skipfps=str(self.lineEdit.text())
        treshold=str(self.lineEdit_2.text())
        return skipfps , treshold

    def abrirred(self):
        self.fileopen(type="red")

    def modoejecucion(self):
        
        if modo == "Imagenes":
            skipfps , tresholdp = self.guardar()
            Ejecucion.Ejecucion_mode(self=self,modo=modo,red=red)
            Ejecucion.Mostrar_img(self=self,fname=fname,brillo=brillo,color=color,cont=cont)
            Ejecucion.Cargaparametros(self=self,pathmodel=red)
            Ejecucion.Inferencia(self=self,img=fname, treshold=tresholdp)
            
        elif modo == "Video":
            print("ejecutando")
            skipfps , treshold = self.guardar()
            self.videodetec = VideoAnalyzer(video_path=fname)
            self.videodetec.start()
            self.videodetec.videoEntered.connect(self.on_video_entered)
            self.videodetec.coutEntered.connect(self.on_count_entered)
                
        elif modo == "Video en Tiempo real":
            skipfps , treshold = self.guardar()
            Ejecucion.Ejecucion_mode(self=self,modo=modo,red=red)
            self.start_video(a=1,videofile=fname)
        
        self.Ejecucion_mode(modo=modo,red=red) 
         
    def start_video(self,a,videofile):
        global b
        fname=videofile
        if a == 1: #previsualizacion videos descargados 
             tiemporeal = True
             self.thread = VideoThread(tiemporeal=tiemporeal,fname=fname)
             self.thread.start()
             self.thread.change_pixmap_signal.connect(self.update_image)
             
        elif a==2: #previsualizacion videos cargados de archivo
            tiemporeal = False
            self.thread = VideoThread(tiemporeal=tiemporeal,fname=fname)
            self.thread.start()
            self.thread.change_pixmap_signal.connect(self.update_image)
            
        elif a==3: #reproducir video en ejecucion
            print("reproduciendo video")
            global b
            b=1
            self.thread = VideoThread(tiemporeal=False,fname=fname)
            self.thread.start()
            self.thread.change_pixmap_signal.connect(self.update_image)
            
    def salir(self):
        sys.exit()
                
    def stop(self):
        self.hilo_corriendo = False
        self.quit()
        
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
        pathout = ConfigColor.configbrillo(self, path=path,brillo=brillo)
        return pathout
    
    def configuracioncontraste(self,path,cont):
        pathout = ConfigColor.configcontraste(self, path=path,contraste=cont)
        return pathout
    
    def configuracioncolor(self,path,color):
        pathout = ConfigColor.configcolor(self, path=path,color=color)
        return pathout
        
    def fileopen(self,type):
        global red, fname,color,cont,brillo,b
        if type =="Video":
            color=1
            cont=1
            brillo=1
            fname,bo = QFileDialog.getOpenFileName(self,"Open File",""," Videos (*.mp4 *.wav)")
            self.lineEdit.setEnabled(True)
            self.frame_3.setDisabled(True)
            self.start_video(a=2,videofile=fname)
            b=0 

        elif type =="Imagenes":
            fname,bo = QFileDialog.getOpenFileName(self,'Open File',''," Imagenes (*.jpg *.jpeg *.png)")
            self.frame_3.setEnabled(True)
            self.lineEdit.setDisabled(True)
            self.label_18.setPixmap(QPixmap(fname))

        elif type == "red":
            pathname,bo = QFileDialog.getOpenFileName(self,'Open File',''," Archivo comprimido (*.zip *.rar)") 
            self.videodetec.Cargaparametros()
            red = pathname
            self.label_28.setText(pathname)

        elif type =="Video en Tiempo real":
            color=1
            cont=1
            brillo=1
            self.url_dialog.exec_()
            self.lineEdit.setEnabled(True)
            self.frame_3.setDisabled(True)
            self.start_video(a=1,videofile=fname)
        
    def Ejecucion_mode(self, modo, red):
        self.label_24.setText(red)
        if modo == "Video":
            self.radioButton_5.setChecked(True)
        elif modo == "Imagenes":
            self.radioButton_6.setChecked(True)
        elif modo == "Video en Tiempo real":
            self.radioButton_4.setChecked(True)  
            
    def filesave(self,data):
        sname,b = QFileDialog.getSaveFileName(self,'Save file','',"Json (*.json)")
        file = open(sname,'w')
        file.write(data)
        file.close()
    
    def configactual(self,data):
        self.textEdit.setPlainText(data)

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
            modo = "Video en Tiempo real"
            type = modo
            self.fileopen(type) 
            self.radioButton_2.setChecked(True)
        return modo
     
    def showdialog(self):
        dialog = ErrorDialog(self)
        dialog.show()
    
    def on_url_entered(self,url):
        global fname
        print(f"URL ingresada: {url}")
        fname = url 
        


if __name__ == "__main__":
    gui = QtWidgets.QApplication([])
    window = MainWindow()
    # asyncio.run(uvi())
    window.show()
    gui.exec_()
