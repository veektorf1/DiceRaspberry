from flask import Flask,redirect,url_for,render_template


def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static')

    from app.routes import main
    app.register_blueprint(main)

    return app