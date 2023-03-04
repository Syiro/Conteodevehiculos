
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import zipfile
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import tensorflow as tf
import numpy as np
from PIL import Image
from imutils.video import FPS
import json
import requests
from datetime import date
from datetime import datetime
from untitled import *
from config import *



class ImageAnalizer(QThread):
    ImgEntered = pyqtSignal(np.ndarray)
    CountImgEntered = pyqtSignal(int)
    
    def __init__(self, photo_path,treshold):
        super(ImageAnalizer, self).__init__()
        self.photo_path = photo_path
        self.treshold = treshold
    
    def Cargaparametros(self,red):
        local_zip = red # sacar a la interfaz
        zip_ref = zipfile.ZipFile(local_zip, "r")
        zip_ref.extractall("fine_tuned_model")
        zip_ref.close()
        global PATH_TO_SAVE_MODEL
        PATH_TO_MODEL_DIR = 'fine_tuned_model/content/fine_tuned_model'
        PATH_TO_SAVE_MODEL = PATH_TO_MODEL_DIR + '/saved_model'
        
    
    
    def run(self):
        
        fps = FPS().start()        
        treshold=float(self.treshold)
        detect_fn = tf.saved_model.load(PATH_TO_SAVE_MODEL)
        #detect_fn = self.Cargaparametros()
        label_map_pbtxt_fname = 'label_map.pbtxt'
        category_index = label_map_util.create_category_index_from_labelmap(
            label_map_pbtxt_fname)
        image_path = self.photo_path
        image_np = np.array(Image.open(image_path))
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = detect_fn(input_tensor)
        # Analizamos cuántas detecciones se obtuvieron
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}

        detections['num_detections'] = num_detections

        detections['detection_classes'] = detections['detection_classes'].astype(
            np.int64)

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
            min_score_thresh=treshold,
            use_normalized_coordinates=True,
        )

        # Visualizamos resultados
        # cv2_imshow(image_np_with_detections)
        im = image_np_with_detections
        
        # self.label_25.setText(num_detections)
        count = 0
        for i in detections['detection_scores']:
            if i > treshold:
                count = count+1
                
        fps.stop()
        
        self.ImgEntered.emit(im)
        self.CountImgEntered.emit(count)
        
        print("Tiempo en empezar a procesar una imagen es : {}".format(fps.elapsed()))
        
        
        url = 'http://127.0.0.1:8000/datossemaforo/'
        pyload = {'fecha':str(datetime.now()),'carrosdetectados':count}
        data=json.dumps(pyload) 
        response = requests.post(url, data)   
        
        if response.status_code == 200:
            print(response.content)   
         