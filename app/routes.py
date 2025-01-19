from flask import render_template, Blueprint,request,url_for,redirect,flash,get_flashed_messages,jsonify
from collections import Counter
import random
from app.Detector.main import DiceDetector,checkLen
from app.Detector.config import model, init_camera
from picamera2 import Picamera2
import json
import threading
import signal
import threading
import cv2

import RPi.GPIO as GPIO
from time import sleep

motor_pin = 19
button_pin = 26
green_pin = 5
yellow_pin = 6
red_pin = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin,GPIO.OUT)
GPIO.setup(button_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green_pin,GPIO.OUT)
GPIO.setup(yellow_pin,GPIO.OUT)
GPIO.setup(red_pin,GPIO.OUT)


main = Blueprint('main',__name__)

NUM_OF_DICES = 5


picam2 = Picamera2()

#picam2.configure(picam2.create_video_configuration(main={"format": 'XRGB8888',
#                                                "size": (640, 480)}))

camera_config = picam2.create_still_configuration(main={"size": (640, 480)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)

'''def closeCamera():
    picam2.close()
atexit.register(closeCamera)'''

picam2.start()
detector = DiceDetector(picam2=picam2)
accuracy_min = 0.5

rolling_phase = False
start_motor = True #TODO - zmienne mające sens przy operowaniu na wątkach
#- teraz raczej mniej ale może do obsługi przerwania któraś by się przydała

DicesResult = None

try_count = 3

def run_motor1(change):
    global start_motor
    start_motor = True

GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=run_motor1, bouncetime=1000)

def GPIO_cleanup():
    GPIO.output(red_pin,0)
    GPIO.output(yellow_pin,0)
    GPIO.output(green_pin,0)
    GPIO.output(motor_pin,0)

def lightDiodes():
    global try_count
    if try_count == 3:
        GPIO.output(red_pin,1)
        GPIO.output(yellow_pin,1)
        GPIO.output(green_pin,1)
    elif try_count == 2:
        GPIO.output(red_pin,1)
        GPIO.output(yellow_pin,1)
        GPIO.output(green_pin,0)
    elif try_count == 1:
        GPIO.output(red_pin,1)
        GPIO.output(yellow_pin,0)
        GPIO.output(green_pin,0)
    elif try_count == 0:
        GPIO.output(red_pin,0)
        GPIO.output(yellow_pin,0)
        GPIO.output(green_pin,0)

lightDiodes()

def camera2() -> list:
    '''
    Function seponsible for detecting dices and returns a result based on validation
    :return: DicesResult - list of dices values integers
    '''
    try:
        global detector
        #global start_motor
        #global rolling_phase
        global DicesResult
        reroll = True
        
        while True:#not stop_thread.is_set():
                
                if reroll:
                    reroll=False


                    print("detect")

                    GPIO.output(motor_pin,1)
                    sleep(3)
                    GPIO.output(motor_pin,0)
                                
                res,frame = detector.detectAndDisplay(accuracy_min)
                print("Result iteration ",res, len(detector.history) )
                detector.validateResult(res)

                if detector.confirmed_result is not None:
                    if checkLen(res) == NUM_OF_DICES: 
                        DicesResult = detector.getFinalResult(res)
                        print(DicesResult)

                        detector.resetHistory()
                        
                        return DicesResult
                    else: # confirmed result but not enough dices detected -> reset history
                        detector.resetHistory()
                        reroll=True


    except KeyboardInterrupt:  
        print("Keyboard interrupt")
        GPIO_cleanup()
        picam2.stop()
    except Exception as e:
        print(f'Error: {e}')
        GPIO_cleanup()
        picam2.stop()
    finally:
        pass
        
        
        
def signal_handler(sig, frame):
    print('Ctrl+C pressed!')
    GPIO_cleanup()
    picam2.stop()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

table_data = [
    {"id": "1", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "2", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "3", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "4", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "5", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "6", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "3x", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "4x", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "3+2x", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "mały strit", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "duży strit", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "generał", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "szansa", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
    {"id": "suma", "player2": 0, "player1": 0, "status": "black-bold", "status2": "black-bold"},
]

table_kostki = [0, 0, 0, 0, 0]
table_selected = [0, 0, 0, 0, 0]
tura = 1

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/result', methods=['GET'])
def get_result():
    return jsonify({'history': detector.history})

@main.route('/get-data')
def get_data():
    return jsonify(table_data)

@main.route('/get-kostki')
def get_kostki():
    return jsonify(table_kostki)


def reset_game():
    global table_data, table_kostki, table_selected, tura, try_count
    table_data = [
        {"id": "1", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "2", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "3", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "4", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "5", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "6", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "3x", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "4x", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "3+2x", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "mały strit", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "duży strit", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "generał", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "szansa", "player2": "", "player1": "", "status": "gray", "status2": "gray"},
        {"id": "suma", "player2": 0, "player1": 0, "status": "black-bold", "status2": "black-bold"},
    ]
    table_kostki=[0,0,0,0,0]
    table_selected=[0,0,0,0,0]
    tura=1
    try_count=3
    lightDiodes()

@main.route('/koniec-gry')
def koniec_gry():
    global table_data, table_kostki, table_selected, tura
    if table_data[13]["player1"] > table_data[13]["player2"]:
        wynik = 1
    elif table_data[13]["player1"] < table_data[13]["player2"]:
        wynik = 2
    else:
        wynik = 0
    reset_game()
    return jsonify({"wynik": wynik})

@main.route('/choose-kostka', methods=['GET'])
def choose_kostka():
    global table_selected
    item_id = int(request.args.get('item_id')[-1]) - 1
    table_selected[item_id] = 1 if table_selected[item_id] == 0 else 0
    return jsonify(success=True)

@main.route('/choose-item', methods=['GET'])
def choose_item():
    global table_data
    global table_selected
    global tura
    global try_count
    cheating = 0
    item_id = int(request.args.get('item_id'))  # Pobieranie parametru z query string
    if tura == 1 and table_data[item_id]["status"] == "gray":
        table_data[item_id]["status"] = "black-bold"
        table_data[13]["player1"] = table_data[13]["player1"]+table_data[item_id]["player1"]
        tura=2
        try_count = 3
        lightDiodes()
    elif tura == 2 and table_data[item_id]["status2"] == "gray":
        table_data[item_id]["status2"] = "black-bold"
        table_data[13]["player2"] = table_data[13]["player2"]+table_data[item_id]["player2"]
        tura=1
        try_count = 3
        lightDiodes()
    else:
        cheating = 1
    if cheating==0:
        table_selected=[0,0,0,0,0]
        for i in range(13):
            if table_data[i]["status2"]=="gray":
                table_data[i]["player2"]=""
            if table_data[i]["status"]=="gray":
                table_data[i]["player1"]=""
        return jsonify(success=True)
    return jsonify(success=False)

@main.route('/update-data')
def update_data():
    global try_count
    if(try_count > 0):
        try_count -= 1
        rzut_koscmi()
        przelicz()
        
    return jsonify(success=True)


def rzut_koscmi():
    global table_kostki, table_selected
    
    lightDiodes()
    result = camera2()
    result_shuffled = random.sample(result, len(result))

    print(f'Confirmed result is {result} ')

    for i in range(5):
        if table_selected[i] == 0:
            
            if i<NUM_OF_DICES:
                table_kostki[i] = result_shuffled[i]
            else:
                table_kostki[i] = random.randint(1, 6)

def przelicz():
    global table_kostki
    global table_data
    global tura
    for i in range(6):
        if tura == 1:
            if table_data[i]["status"]=="gray":
                table_data[i]["player1"]=sum([x for x in table_kostki if x == i+1])
        else:
            if table_data[i]["status2"]=="gray":
                table_data[i]["player2"]=sum([x for x in table_kostki if x == i+1])
    suma=sum(table_kostki)
    ilosc = Counter(table_kostki).most_common()
    sum_3x = 0
    sum_4x = 0
    sum_5x = 0
    sum_3x2x = 0
    posortowana=sorted(table_kostki)
    print(posortowana)
    if ilosc[0][1]>2:
        sum_3x = suma
        if ilosc[0][1]>3:
            sum_4x = suma
            if ilosc[0][1]>4:
                sum_5x = 50
        if len(ilosc)>1 and ilosc[1][1]>1:
            sum_3x2x = 25
    streak = 0
    for i,x in enumerate(posortowana[:4]):
        if posortowana[i+1]==x+1: 
            streak += 1
        elif posortowana[i+1]>x+1:
            if i>=2:
                break
            else:
                streak = 0


    if tura == 1:
        if table_data[6]["status"]=="gray":
            table_data[6]["player1"]=sum_3x
        if table_data[7]["status"]=="gray":
            table_data[7]["player1"]=sum_4x
        if table_data[8]["status"]=="gray":
            table_data[8]["player1"]=sum_3x2x
        if table_data[11]["status"]=="gray":
            table_data[11]["player1"]=sum_5x
        if table_data[12]["status"]=="gray":
            table_data[12]["player1"]=suma
        if table_data[9]["status"]=="gray" and streak>=3:
            table_data[9]["player1"]=30
        elif table_data[9]["status"]=="gray":
            table_data[9]["player1"]=0
        if table_data[10]["status"]=="gray" and streak==4:
            table_data[10]["player1"]=40
        elif table_data[10]["status"]=="gray":
            table_data[10]["player1"]=0
    else:
        if table_data[6]["status2"]=="gray":
            table_data[6]["player2"]=sum_3x
        if table_data[7]["status2"]=="gray":
            table_data[7]["player2"]=sum_4x
        if table_data[8]["status2"]=="gray":
            table_data[8]["player2"]=sum_3x2x
        if table_data[11]["status2"]=="gray":
            table_data[11]["player2"]=sum_5x
        if table_data[12]["status2"]=="gray":
            table_data[12]["player2"]=suma
        if table_data[9]["status2"]=="gray" and streak >=3:
            table_data[9]["player2"]=30
        elif table_data[9]["status2"]=="gray":
            table_data[9]["player2"]=0
        if table_data[10]["status2"]=="gray" and streak==4:
            table_data[10]["player2"]=40
        elif table_data[10]["status2"]=="gray":
            table_data[10]["player2"]=0
 