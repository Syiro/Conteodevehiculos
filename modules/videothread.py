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


class VideoAnalyzer(QThread):
    videoEntered = pyqtSignal(np.ndarray)
    coutEntered = pyqtSignal(int)
    
    def __init__(self, video_path,skipfps,treshold):
        super(VideoAnalyzer, self).__init__()
        self.video_path = video_path
        self.skipfps = skipfps
        self.treshold = treshold
    
    def Cargaparametros(self):
        local_zip = "fine_tuned_model.zip"  # sacar a la interfaz
        zip_ref = zipfile.ZipFile(local_zip, "r")
        zip_ref.extractall("fine_tuned_model")
        zip_ref.close()
        PATH_TO_MODEL_DIR = 'fine_tuned_model/content/fine_tuned_model'
        PATH_TO_SAVE_MODEL = PATH_TO_MODEL_DIR + '/saved_model'
        return PATH_TO_SAVE_MODEL
        PATH_TO_SAVE_MODEL = 'fine_tuned_model/content/fine_tuned_model/saved_model'
    
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
              
        #PATH_OUTPUT = "videocondetecciones.mp4"  # sacar a la interfaz

       

        TRESHOLD = float(self.treshold) # sacar a la interfaz

        

        #writer = None

        W = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
        H = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fpsreal = int(vs.get(cv2.CAP_PROP_FPS))
        ct = CentroidTracker(maxDisappeared=40, maxDistance=50)


        fpsskip = int(self.skipfps)
        SKIP_FPS =int(self.skipfps) # sacar a la interfaz

        
        trackers = []
        trackableObjects = {}

        totalFrame = 0
        totaldeteccions = 0
        totalDown = 0
        totalUP = 0

        DIRECTION_PEOPLE = True

        POINT = [0, int((H*(9/10))-H*0.1), W, int(H*0.1)]

        PATH_TO_SAVE_MODEL = 'fine_tuned_model/content/fine_tuned_model/saved_model'

        #fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        #writer = cv2.VideoWriter(PATH_OUTPUT, fourcc, 20.0, (W, H), True)
        
        detect_fn = tf.saved_model.load(PATH_TO_SAVE_MODEL)
        
        
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


            #writer.write(frame)

            
            totalFrame += 1
            
            if totalFrame == 1 :
                fps.update()
                fps.stop()
            
            #print(totaldeteccions)
            self.videoEntered.emit(frame)
            self.coutEntered.emit(totalUP)
            
            #print(totalFrame)

        vs.release()
        fps2.stop()
                

            
        print("Tiempo en empezar a procesar es : {}".format(fps.elapsed()))
        print("Tiempo por frame {}".format(fps.fps()))
        print("Tiempo total de procesado es:{}".format(fps2.elapsed()))
        
        
        
        count = totalUP
        url = 'http://127.0.0.1:8000/datossemaforo/'
        pyload = {'fecha':str(datetime.now()),'carrosdetectados':count}
        data=json.dumps(pyload) 
        response = requests.post(url, data)   
        
        if response.status_code == 200:
            print(response.content)   
        
       
    
        #writer.release()

        