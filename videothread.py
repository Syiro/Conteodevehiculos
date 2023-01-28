
import sys
import os
import requests
import cv2
import numpy as np

from config import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class VideoThread(QThread):
    
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self,):
        super().__init__()
        self.__run_flag= True
    
    def stop(self):
        self.__run_flag= False
        self.wait()

    def run(self):
        # capture from web cam

        cap = cv2.VideoCapture(0)
        while self.__run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        
        cap.release()

class VideoConvert(VideoThread):

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        Image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        #flip = cv2.flip(Image,1)
        convertir_QT = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
        pic = convertir_QT.scaled(800, 600, Qt.KeepAspectRatio)
        return QPixmap.fromImage(pic)

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        # if b==1:
        self.label_18.setPixmap(qt_img)
            
        # else :
        #     self.label_26.setPixmap(qt_img) 
        

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()
