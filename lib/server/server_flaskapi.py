from flask import Flask
from flask_cors import CORS


def flask_app():
    app = Flask(__name__)
    CORS(app)
    return app
