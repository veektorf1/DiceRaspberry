from app import create_app
import os

app_flask  = create_app()

if __name__ == '__main__':
    app_flask.run(debug=True,host='0.0.0.0')