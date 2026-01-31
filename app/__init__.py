from flask import Flask
from app.db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.py")

    # register blueprints


    # db removal after requests
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.remove()

    return app