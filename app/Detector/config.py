from picamera2 import Picamera2
from ultralytics import YOLO
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
modelpath = os.path.join(script_dir, 'best_final.pt')

model = YOLO(modelpath) # model yolov8n 


height =480
width=640
middle =((width//2),(height//2))

def init_camera():
    
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"format": 'XRGB8888',
                                                      "size": (width, height)}))
    picam2.start()
    return picam2

def get_frame(picam2: Picamera2) -> np.ndarray:
    frame = picam2.capture_array()[:,:,:3]
    return frame
