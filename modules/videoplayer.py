from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import pafy
import cv2
import zipfile
from untitled import *


class VideoThread(QThread):
    
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self,fname,tiemporeal):
        
        super().__init__()
        self.__run_flag= True
        self.tiemporeal=tiemporeal
        self.fname=fname
        
    def stop(self):
        self.__run_flag = False
        self.wait()

    def run(self):
        if self.__run_flag == False:
            cv_img = None
        else:   
            if self.tiemporeal==True: #video de youtube
                #aca leo el video cargado y lo proceso
                video = pafy.new(self.fname)
                best = video.getbest(preftype='mp4')
                cap = cv2.VideoCapture(best.url)
                
                while True:
                    ret, cv_img = cap.read()
                    if cv_img is None :
                        break  
                        #hilo de analizis de video guardado
                    self.change_pixmap_signal.emit(cv_img)
                cap.release()
                
            else:  #archivo de video
                cap = cv2.VideoCapture(self.fname)
                
                while True:
                    ret, cv_img = cap.read()
                    
                    if cv_img is None:
                        break
                    
                    self.change_pixmap_signal.emit(cv_img)

                cap.release() 
                
            
