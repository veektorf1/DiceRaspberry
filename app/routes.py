from flask import render_template, Blueprint,request,url_for,redirect,flash,get_flashed_messages,jsonify
from app.Detector.main import DiceDetector 
from app.Detector.config import model, init_camera
from picamera2 import Picamera2
import json
import threading
import signal
import threading
import cv2

main = Blueprint('main',__name__)

data='123'

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"format": 'XRGB8888',
                                                    "size": (640, 480)}))
picam2.start()
detector = DiceDetector(picam2=picam2)
stop_thread = threading.Event()

def thread_camera():
    
    while not stop_thread.is_set():
        accuracy_min = 0.5
        res,frame = detector.detectAndDisplay(accuracy_min)
        detector.validateResult(res)

        if detector.confirmed_result is not None:
            print(f'Confirmded result is {res} ')
            detector.printResult(res)

            # sleep(5)
            detector.resetHistory()

    cv2.destroyAllWindows()

def signal_handler(sig, frame):
    print('Ctrl+C pressed!')
    stop_thread.set()
    t1.join()
    picam2.stop()
    exit(0)


t1 = threading.Thread(target=thread_camera)
t1.start()
signal.signal(signal.SIGINT, signal_handler)

@main.route('/',methods=['GET','POST'])
def index():
    
    json_data = {'history': 'json'}
    json_data = get_result()
    return render_template('index.html', data=json_data)


@main.route('/api/result', methods=['GET'])
def get_result():
    return jsonify({'history': detector.history})
