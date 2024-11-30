from flask import Flask,redirect,url_for,render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment



bootstrap = Bootstrap()
moment = Moment()

def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static')

    moment.init_app(app)
    bootstrap.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app