import json
import requests
from configcolor import*
from app import Conexion, main, models, schemas
from untitled import *
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QPushButton, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import zipfile
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import tensorflow as tf
#import tensorflow_io as tfio
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
#from google.colab.patches import cv2_imshow

class Ejecucion:
    def __init__(self):
        pass
    def Ejecucion_mode(self,modo,red):
        self.label_24.setText(red)
        if modo=="Video":
            self.radioButton_5.setChecked(True)
        elif modo=="Imagenes":
            self.radioButton_6.setChecked(True)
        elif modo=="Video en Tiempo real":
            self.radioButton_4.setChecked(True)
            
            
    def Inferencia(self,img):
        
        local_zip = "fine_tuned_model.zip"
        zip_ref = zipfile.ZipFile(local_zip, "r")
        zip_ref.extractall("fine_tuned_model")
        zip_ref.close()
        PATH_TO_MODEL_DIR = 'fine_tuned_model/content/fine_tuned_model'
        PATH_TO_SAVE_MODEL = PATH_TO_MODEL_DIR + '/saved_model'
        detect_fn = tf.saved_model.load(PATH_TO_SAVE_MODEL)
        label_map_pbtxt_fname = 'label_map.pbtxt'
        category_index = label_map_util.create_category_index_from_labelmap(label_map_pbtxt_fname)
        image_path = img
        image_np = np.array(Image.open(image_path))
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = detect_fn(input_tensor)
        # Analizamos cuántas detecciones se obtuvieron
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0,:num_detections].numpy() for key, value in detections.items()}

        detections['num_detections'] = num_detections

        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        # Tomamos una imagen y la copiamos para dibujar los bounding box
        image_np_with_detections = image_np.copy()

        # Utilizamos la libreria de obejct detection para visualizar le bounding box y la clasificación
        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'],
            detections['detection_scores'],
            category_index,
            max_boxes_to_draw=200,
            min_score_thresh=0.40,
            use_normalized_coordinates = True,
        )


        # Visualizamos resultados
        #cv2_imshow(image_np_with_detections)
        im = Image.fromarray(image_np_with_detections)
        im.save("imagencondetecciones.jpg")
        self.label_26.setPixmap(QPixmap("imagencondetecciones.jpg"))
        #self.label_25.setText(num_detections)
        count=0
        for i in detections['detection_scores']:
            if i > 0.40:
                count=count+1
        self.label_25.setText(str(count))
       
        
    def Mostrar_img(self,fname,brillo,color,cont):
        self.label_26.setPixmap(QPixmap(self.configuracionbrillo(fname,brillo)))
        self.label_26.setPixmap(QPixmap(self.configuracioncolor(fname,color)))
        self.label_26.setPixmap(QPixmap(self.configuracioncontraste(fname,cont)))
        
    