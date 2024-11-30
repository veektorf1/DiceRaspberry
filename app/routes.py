from flask import render_template, Blueprint,request,url_for,redirect,flash,get_flashed_messages

main = Blueprint('main',__name__)

@main.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')
 