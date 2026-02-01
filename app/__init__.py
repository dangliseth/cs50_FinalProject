from flask import Flask

from flask_login import LoginManager
from app.models import Users

from app.db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    # initialize login manager for authentications
    login_manager = LoginManager()
    login_manager.login_view = "auth.login" # type: ignore
    login_manager.init_app(app)
    # user loader
    # get user id from db
    @login_manager.user_loader
    def load_user(user_id):
        return db.query(Users).get(int(user_id))
    
    # register blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    # db removal after requests
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.remove()

    return app