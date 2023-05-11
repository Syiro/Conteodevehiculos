import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import zipfile
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import tensorflow as tf
import numpy as np
import time
from PIL import Image
from imutils.video import FPS
from imutils.video import VideoStream
from centroidtracker import CentroidTracker
from trackableobject import TrackableObject
import dlib
import json
import os
import requests
from datetime import date
from datetime import datetime
from untitled import *
from config import *
import pafy
from urllib.parse import urlparse
import mysql.connector

class VideoAnalyzer(QThread):
    videoEntered = pyqtSignal(np.ndarray)
    coutEntered = pyqtSignal(int)
    
    def __init__(self, video_path,skipfps,treshold,vmax):
        super(VideoAnalyzer, self).__init__()
        self.video_path = video_path
        self.skipfps = skipfps
        self.treshold = treshold
        self.vmax = vmax
    
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
        fps2 = FPS().start()
        PATH_VIDEO = self.video_path
        parsed = urlparse(PATH_VIDEO)

        if parsed.scheme == "http" or parsed.scheme == "https":
             video = pafy.new(PATH_VIDEO)
             best = video.getbest(preftype='mp4')
             vs = cv2.VideoCapture(best.url)
        else:
             vs = cv2.VideoCapture(PATH_VIDEO)
             
        category_index = label_map_util.create_category_index_from_labelmap("label_map.pbtxt", use_display_name=True)
        TRESHOLD = float(self.treshold) # sacar a la interfa
        W = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
        H = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))
        ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
        SKIP_FPS =int(self.skipfps) # sacar a la interfaz
        trackers = []
        trackableObjects = {}
        rects = []
        totalFrame = 0
        totaldeteccions = 0
        totalUP = 0
        detect_fn = tf.saved_model.load(PATH_TO_SAVE_MODEL)
        countedObjects = {}
        speed=0
        while True:
            
            ret, frame = vs.read()
                        
            if frame is None:
                

                break

            status = "Waiting"
            rects = []

            if totalFrame % SKIP_FPS == 0:
                status = "Detecting"
                totaldeteccions += 1
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
                    

            objects = ct.update(rects)
            
            for (objectID, centroid) in objects.items():
                
                MIN_SPEED = int(self.vmax)
                
                to = trackableObjects.get(objectID, None)
                if to is None:
                    to = TrackableObject(objectID, centroid)

                else:
                    y = [c[1] for c in to.centroids]
                    direction = centroid[1] - np.mean(y)
                    to.centroids.append(centroid) 
                    if not to.counted:
                        dist = np.linalg.norm(np.array(to.centroids[-1]) - np.array(to.centroids[-2]))
                        speed = (dist / SKIP_FPS)*100
                        if direction < 0 and speed < MIN_SPEED:
                            if objectID not in countedObjects:
                                totalUP += 1
                                countedObjects[objectID] = True
                            to.counted = True
                                                        
                trackableObjects[objectID] = to
                #text = "{}: {:.2f}%".format(category_index[idx]['name'], detection_scores[objectID]*100
                text = "{}: {:.1f}px/f, {:.2f}".format(category_index[idx]['name'], speed, detection_scores[objectID])
                if objectID < len(rects):
                    (startX, startY, endX, endY) = rects[objectID]
                cv2.putText(frame, text, (startX, startY-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0 ,255, 0), 2)
                if category_index[idx]['name'] == 'vehicle':
                        color = (0, 255, 0)  # verde para "vehicle"
                else:
                    color = (255, 0, 0)  # azul para "novehicle"
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

            info = [
                ("Carros detectados", totalUP),
                ("Estado", status),
            ]

            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, H - ((i*20) + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


            #writer.write(frame)

            
            totalFrame += 1
            fps2.update()
            if totalFrame == 1 :
                
                fps.stop()
            
            #print(totaldeteccions)
            self.videoEntered.emit(frame)
            self.coutEntered.emit(totalUP)
            
            #print(totalFrame)

        vs.release()
        fps2.stop()
                

            
        print("Tiempo en empezar a procesar es : {}".format(fps.elapsed()))
        print("Frames por segundo {}".format(fps2.fps()))
        print("Tiempo total de procesado es:{}".format(fps2.elapsed()))
        
        
        ultimousuario = self.ultimousuario()
        ultimousuario=int(ultimousuario)
        count = totalUP
        url = 'http://127.0.0.1:8000/datossemaforo/'
        pyload = {'idcarros':ultimousuario,'fecha':str(datetime.now()),'carrosdetectados':count}
        data=json.dumps(pyload) 
        response = requests.post(url, data)   
        
        if response.status_code == 200:
            print(response.content) 
            
    def ultimousuario(self):
            # Conexión a la base de datos
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Syiro2101.",
        database="mydb"
        )

    # Crear cursor
        cursor = mydb.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT idusuarios FROM usuarios ORDER BY idusuarios DESC LIMIT 1;")
        result = cursor.fetchone()
        return result[0]
        
    

    #writer.release()

    