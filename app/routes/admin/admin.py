from flask import Blueprint, render_template

bp = Blueprint("admin", __name__, template_folder="templates")

@bp.route("/home")
def home():
    return render_template("home.html")