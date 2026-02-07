from flask import Flask

from flask_login import LoginManager
from app.models import Users

from app.db import db

import re

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

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
    from app.routes.auth.auth import bp as auth_bp
    from app.routes.admin.admin import bp as admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # have a humanize function for templates
    def humanize_label(value):
        # handle camel cases: "firstName" -> "First Name"
        value = re.sub(r"(?<!^)(?=[A-Z])", " ", value)

        # handle snake_cases: "first_name" -> "First Name"
        value = value.replace("_", " ")

        return value.title()
    
    # add humanize_function into templates as humanize
    app.add_template_filter(humanize_label, "humanize")

    # db removal after requests
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.remove()

    return app