import json
import os
import requests
from configcolor import *
from videoplayer import*
import sys
sys.path.append('/code/app')
#import app 
#from app import Conexion, main, models, schemas
from untitled import *
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QPushButton, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import zipfile
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import tensorflow as tf
# import tensorflow_io as tfio
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
# from google.colab.patches import cv2_imshow
import numpy as np
import imutils
import time
import dlib
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from imutils.video import VideoStream
from imutils.video import FPS
from centroidtracker import CentroidTracker
from trackableobject import TrackableObject
from datetime import date
from datetime import datetime
import pafy
import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import time


class Ejecucion:

    def Ejecucion_mode(self, modo, red):
        self.label_24.setText(red)
        if modo == "Video":
            self.radioButton_5.setChecked(True)
        elif modo == "Imagenes":
            self.radioButton_6.setChecked(True)
        elif modo == "Video en Tiempo real":
            self.radioButton_4.setChecked(True)

    def Cargaparametros(self, pathmodel):
        local_zip = pathmodel  # sacar a la interfaz
        zip_ref = zipfile.ZipFile(local_zip, "r")
        zip_ref.extractall("fine_tuned_model")
        zip_ref.close()
        global PATH_TO_SAVE_MODEL
        PATH_TO_MODEL_DIR = 'fine_tuned_model/content/fine_tuned_model'
        PATH_TO_SAVE_MODEL = PATH_TO_MODEL_DIR + '/saved_model'
        
    def Inferencia(self, img , treshold):
        
        treshold=float(treshold)
        detect_fn = tf.saved_model.load(PATH_TO_SAVE_MODEL)
        #detect_fn = self.Cargaparametros()
        label_map_pbtxt_fname = 'label_map.pbtxt'
        category_index = label_map_util.create_category_index_from_labelmap(
            label_map_pbtxt_fname)
        image_path = img
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
        im = Image.fromarray(image_np_with_detections)
        im.save("imagencondetecciones.jpg")
        self.label_26.setPixmap(QPixmap("imagencondetecciones.jpg"))
        # self.label_25.setText(num_detections)
        count = 0
        for i in detections['detection_scores']:
            if i > treshold:
                count = count+1
        
        url = 'http://127.0.0.1:8000/datossemaforo/'
        pyload = {'fecha':str(datetime.now()),'carrosdetectados':count}
        data=json.dumps(pyload) 
        response = requests.post(url, data)   
        
        if response.status_code == 200:
            print(response.content)   
         
        self.label_25.setText(str(count))

    def Mostrar_img(self, fname, brillo, color, cont):
        self.label_26.setPixmap(
            QPixmap(self.configuracionbrillo(fname, brillo)))
        self.label_26.setPixmap(QPixmap(self.configuracioncolor(fname, color)))
        self.label_26.setPixmap(
            QPixmap(self.configuracioncontraste(fname, cont)))
        
    def Inferencia_video(self, img, skipfps, treshold):
        
        
        PATH_VIDEO = img

        PATH_OUTPUT = "videocondetecciones.mp4"  # sacar a la interfaz

        SKIP_FPS = skipfps  # sacar a la interfaz

        TRESHOLD = treshold # sacar a la interfaz

        vs = cv2.VideoCapture(PATH_VIDEO)

        writer = None

        W = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
        H = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))

        ct = CentroidTracker(maxDisappeared=40, maxDistance=50)

        trackers = []
        trackableObjects = {}

        totalFrame = 0
        totalDown = 0
        totalUP = 0

        DIRECTION_PEOPLE = True

        POINT = [0, int((H*(9/10))-H*0.1), W, int(H*0.1)]

        fps = FPS().start()

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(PATH_OUTPUT, fourcc, 20.0, (W, H), True)
        detect_fn = tf.saved_model.load(PATH_TO_SAVE_MODEL)
        #detect_fn = self.Cargaparametros(pathmodel=pathmodelg)
        while True:

            ret, frame = vs.read()

            
            if frame is None:
                break

            status = "Waiting"
            rects = []

            if totalFrame % SKIP_FPS == 0:
                status = "Detecting"
                trackers = []

                image_np = np.array(frame)
                input_tensor = tf.convert_to_tensor(image_np)
                input_tensor = input_tensor[tf.newaxis, ...]
                detections = detect_fn(input_tensor)
                detection_scores = np.array(detections["detection_scores"][0])
                detection_clean = [
                    x for x in detection_scores if x >= TRESHOLD]

                for x in range(len(detection_clean)):
                    idx = int(detections['detection_classes'][0][x])

                    ymin, xmin, ymax, xmax = np.array(
                        detections['detection_boxes'][0][x])
                    box = [xmin, ymin, xmax, ymax] * np.array([W, H, W, H])

                    (startX, startY, endX, endY) = box.astype("int")

                    tracker = dlib.correlation_tracker()
                    rect = dlib.rectangle(startX, startY, endX, endY)
                    tracker.start_track(frame, rect)

                    trackers.append(tracker)
            else:
                for tracker in trackers:
                    status = "Tracking"

                    tracker.update(frame)
                    pos = tracker.get_position()

                    startX = int(pos.left())
                    startY = int(pos.top())
                    endX = int(pos.right())
                    endY = int(pos.bottom())

                    rects.append((startX, startY, endX, endY))
                    
            cv2.rectangle(frame, (POINT[0], POINT[1]), (POINT[0] +
                          POINT[2], POINT[1] + POINT[3]), (255, 0, 255), 2)

            objects = ct.update(rects)

            for (objectID, centroid) in objects.items():
                to = trackableObjects.get(objectID, None)
                if to is None:
                    to = TrackableObject(objectID, centroid)

                else:
                    y = [c[1] for c in to.centroids]
                    direcction = centroid[1] - np.mean(y)
                    to.centroids.append(centroid)
                    if not to.counted:
                        if centroid[0] > POINT[0] and centroid[0] < (POINT[0] + POINT[2]) and centroid[1] > POINT[1] and centroid[1] < (POINT[1]+POINT[3]):
                            if DIRECTION_PEOPLE:
                                if direcction > 0 :
                                    totalUP += 1
                                    to.counted = True
                            else:
                                if direcction < 0:
                                    totalUP += 1
                                    to.counted = True
                trackableObjects[objectID] = to

                text = "ID {}".format(objectID)
                cv2.putText(frame, text, (centroid[0]-10, centroid[1]-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(
                    frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

            info = [
                ("Carros detectados", totalUP),
                ("Estado", status),
            ]

            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, H - ((i*20) + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


            writer.write(frame)

            
            totalFrame += 1
            
            #time.sleep(0.05)

        fps.stop()

        print("Tiempo completo {}".format(fps.elapsed()))
        print("Tiempo aproximado por frame {}".format(fps.fps()))
        
        # Cerramos el stream the almacenar video y de consumir el video.
        #writer.release()
        vs.release()
        
        count = totalUP
        url = 'http://127.0.0.1:8000/datossemaforo/'
        pyload = {'fecha':str(datetime.now()),'carrosdetectados':count}
        data=json.dumps(pyload) 
        response = requests.post(url, data)   
        
        if response.status_code == 200:
            print(response.content)   
         
        self.label_26.setText(str(count))
    
    def Inferencia_video2(self,img, skipfps, treshold):
        cap = cv2.VideoCapture(img)
        
        writer = None
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        detect_fn = tf.saved_model.load(PATH_TO_SAVE_MODEL)
        writer = cv2.VideoWriter("videodetect.mp4", fourcc, 20.0, (W, H), True)
        totalFrame=0
        
        while True:
            ret,frame = cap.read()
            image_np=np.array(frame)
            if frame is None:
                break
            
            treshold=float(treshold)
            #detect_fn = self.Cargaparametros()
            label_map_pbtxt_fname = 'label_map.pbtxt'
            category_index = label_map_util.create_category_index_from_labelmap(
                label_map_pbtxt_fname)
            
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
            count = 0
            for i in detections['detection_scores']:
                if i > treshold:
                    count = count+1
            totalFrame += 1  
            print(totalFrame)
            writer.write(frame)
            self.filename="videodetect.mp4"
            os.chmod(self.filename, 0o600)
            if os.path.exists(self.filename) and os.path.getsize(self.filename) > 0:
                self.start_video(a=3,videofile=frame)
            else:
                time.sleep(1)
            
            
            
        url = 'http://127.0.0.1:8000/datossemaforo/'
        pyload = {'fecha':str(datetime.now()),'carrosdetectados':count}
        data=json.dumps(pyload) 
        response = requests.post(url, data)   
        
        if response.status_code == 200:
            print(response.content)   
        
        self.label_25.setText(str(count))
