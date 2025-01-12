from flask import render_template, Blueprint,request,url_for,redirect,flash,get_flashed_messages,jsonify
from collections import Counter
import random

main = Blueprint('main',__name__)

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

@main.route('/get-data')
def get_data():
    return jsonify(table_data)

@main.route('/get-kostki')
def get_kostki():
    return jsonify(table_kostki)


def reset_game():
    global table_data, table_kostki, table_selected, tura
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
    cheating = 0
    item_id = int(request.args.get('item_id'))  # Pobieranie parametru z query string
    if tura == 1 and table_data[item_id]["status"] == "gray":
        table_data[item_id]["status"] = "black-bold"
        table_data[13]["player1"] = table_data[13]["player1"]+table_data[item_id]["player1"]
        tura=2
    elif tura == 2 and table_data[item_id]["status2"] == "gray":
        table_data[item_id]["status2"] = "black-bold"
        table_data[13]["player2"] = table_data[13]["player2"]+table_data[item_id]["player2"]
        tura=1
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
    rzut_koscmi()
    przelicz()
    return jsonify(success=True)

def rzut_koscmi():
    global table_kostki, table_selected
    for i in range(5):
        if table_selected[i] == 0:
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
    print(posortowana);
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
 