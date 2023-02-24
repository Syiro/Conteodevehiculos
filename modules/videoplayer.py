from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import pafy
import cv2
import zipfile
from ejecucion import*
from untitled import *
class VideoThread(QThread):
    
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self,fname,tiemporeal):
        
        super().__init__()
        self.__run_flag= True
        self.tiemporeal=tiemporeal
        self.fname=fname
        
    def stop(self):
        self.__run_flag= False
        self.wait()
    
    def Cargaparametros(self):
        
        local_zip = "fine_tuned_model.zip"  # sacar a la interfaz
        zip_ref = zipfile.ZipFile(local_zip, "r")
        zip_ref.extractall("fine_tuned_model")
        zip_ref.close()
        global PATH_TO_SAVE_MODEL
        PATH_TO_MODEL_DIR = 'fine_tuned_model/content/fine_tuned_model'
        PATH_TO_SAVE_MODEL = PATH_TO_MODEL_DIR + '/saved_model'

    def run(self):
        
        if self.tiemporeal==True: #video de youtube
            #aca leo el video cargado y lo proceso
            video = pafy.new(self.fname)
            best = video.getbest(preftype='mp4')
            cap = cv2.VideoCapture(best.url)
            
            while self.__run_flag:
                 ret, cv_img = cap.read()
                 if ret:
                    #hilo de analizis de video guardado
                    self.change_pixmap_signal.emit(cv_img)
            cap.release()
            
        else:  #archivo de video
            cap = cv2.VideoCapture(self.fname)
            while self.__run_flag:
                ret, cv_img = cap.read()
                if ret:
                    #hilo de analizis de 
                    self.change_pixmap_signal.emit(cv_img)
            cap.release()        
