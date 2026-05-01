from flask import Blueprint

bp = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

# Import routes to register them with the blueprint
from . import admin_views, admin_actions