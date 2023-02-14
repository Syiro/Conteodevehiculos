import asyncio
import json
import sys
import os
import requests
import uvicorn

from configcolor import*
#from video import*
from ejecucion import *

from app import Conexion, main, models, schemas
from untitled import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import numpy as np
#export QT_QPA_PLATFORM=xcb
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["QT_QPA_PLATFORM"] = "xcb"

class VideoThread(QThread):
    
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.__run_flag= True
    
    def stop(self):
        self.__run_flag= False
        self.wait()

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(fname)
        while self.__run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        
        cap.release()


# class Worker(QObject):
#     #signals of thread
#     Imageupd = pyqtSignal(QImage)
#     # @pyqtSlot()
#     #long task
#     @pyqtSlot(QImage)
#     def run(self):
#         self.hilo_corriendo = True
#         cap = cv2.VideoCapture(fname)
#         while self.hilo_corriendo:
#             ret, frame = cap.read()
#             if ret:
#                 Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 #flip = cv2.flip(Image, 1)
#                 convertir_QT = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
            
#                 pic = convertir_QT.scaled(800, 600, Qt.KeepAspectRatio)
#                 self.Imageupd.emit(pic)
                

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
           
        self.setupUi(self)
        #text edit implment
        
        # comobo BOx implement

        self.comboBox.activated.connect(self.modo)
       # self.comboBox_4.activated.connect(self.red)

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
        
        # stop button implement
        
        self.pushButton_13.clicked.connect(self.cancel)

        #selec red implement

        self.pushButton.clicked.connect(self.abrirred)

        #guardar button implement

        self.pushButton_2.clicked.connect(self.guardar)
        
        self.pushButton_6.clicked.connect(self.auto)

       # self.pushButton_7.clicked.connect(self.reseteo)
    
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
            self.enviar()
        elif modo == "Video":
            self.enviarvideo()

        

    def reseteo(self):


        pass

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        if b==1:
            self.label_18.setPixmap(qt_img)
            
        else :
            self.label_26.setPixmap(qt_img) 

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        Image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        #flip = cv2.flip(Image,1)
        convertir_QT = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
        pic = convertir_QT.scaled(800, 600, Qt.KeepAspectRatio)
        return QPixmap.fromImage(pic)
        
        # Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # flip = cv2.flip(Image, 1)
        # convertir_QT = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
        # pic = convertir_QT.scaled(800, 600, Qt.KeepAspectRatio)
        #convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        #p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        

    def closeEvent(self, event):
        self.thread.stop()
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
            Ejecucion.Ejecucion_mode(self=self,modo=modo,red=red)
            Ejecucion.Mostrar_img(self=self,fname=fname,brillo=brillo,color=color,cont=cont)
            Ejecucion.Inferencia(self=self,img=fname)
            
        elif modo == "Video":
            print("variables"+str(self.guardar()))
            skipfps , treshold = self.guardar()
            Ejecucion.Ejecucion_mode(self=self,modo=modo,red=red)
            Ejecucion.Inferencia_video(self=self,img=fname, skipfps=int(skipfps), treshold=float(treshold))
            self.start_video(a=1)
    

 
         
    def start_video(self,a):
        self.thread = VideoThread()
        self.thread.start()
        global b , fname
        if a == 1:
             b=2
             fname = "videocondetecciones.mp4"
             
             self.thread.change_pixmap_signal.connect(self.update_image)
             
        else:
           
            b=1
            self.thread.change_pixmap_signal.connect(self.update_image)
  
        a=0
        #self.thread.finished.connect()
 
    # def Imageupd_slotpre(self, Image):
    #     self.label_18.setPixmap(QPixmap.fromImage(Image))               

    # def Imageupd_slot(self, Image):
    #     self.label_26.setPixmap(QPixmap.fromImage(Image))

    def cancel(self):
        self.label_26.clear()
        #self.cap.release()

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
        global fname
        if type =="Video":
            color=1
            cont=1
            brillo=1
            fname,b = QFileDialog.getOpenFileName(self,"Open File",""," Videos (*.mp4 *.wav)")
            self.frame_3.setDisabled(True)
            self.start_video(a=2) 

        elif type =="Imagenes":
            fname,b = QFileDialog.getOpenFileName(self,'Open File',''," Imagenes (*.jpg *.jpeg *.png)")
            self.frame_3.setEnabled(True)
            self.label_18.setPixmap(QPixmap(fname))

        elif type == "red":
            pathname,b = QFileDialog.getOpenFileName(self,'Open File',''," Archivo comprimido (*.zip *.rar)") 
            Ejecucion.Cargaparametros(self,pathmodel=pathname)
            global red
            red = pathname
            self.label_28.setText(pathname)

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

    # def red(self):
    #     global red
    #     combobox = self.sender()
    #     if combobox.currentText() == "SSD Movilnet 2.0 fpnlite":
    #         red = "SSD Movilnet 2.0 fpnlite"
    #     if combobox.currentText() == "Red2":
    #         red = "Red2"
    #     if combobox.currentText() == "Red3":
    #         red = "Red3"

    def enviar(self):
            if modo=="Video":
                self.enviarvideo()
            else:
                try:
                    modo
                    red
                    brillo
                    cont
                    color
                    skipfps 
                    treshold
                except NameError: 
                    self.textEdit.setPlainText("Modo de ejecucion no definido apropiadamente")
                    self.showdialog()
                else:

                    url = 'http://127.0.0.1:8000/configuracion/'
                    pyload = {'brillo': brillo, 'contraste': cont,
                            'color': color, 'modo': modo, 'redneuronal': red , 'skipfps': skipfps, 'treshold':treshold}
                    data=json.dumps(pyload)
                    data2=json.dumps(pyload,indent=6,sort_keys=True,separators =(". ", " = "))
                    response = requests.post(url, data)
                    self.configactual(data2)
                    self.filesave(data)
                    if response.status_code == 200:
                        print(response.content)
                    
    def enviarvideo(self):
        
            if modo== "Video":
                color=1
                cont=1
                brillo=1

            try:
                modo
                red
                brillo
                cont
                color
                skipfps
                treshold
            except NameError: 
                self.textEdit.setPlainText("Modo de ejecucion no definido apropiadamente")
                self.showdialog()
            else:

                url = 'http://127.0.0.1:8000/configuracion/'
                pyload = {'brillo': brillo, 'contraste': cont,
                        'color': color, 'modo': modo, 'redneuronal': red ,'skipfps': skipfps, 'treshold':treshold}
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
