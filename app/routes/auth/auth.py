from flask import Blueprint, render_template, request, redirect, flash, url_for

from flask_login import login_user, logout_user, login_required, current_user
from app.db import db
from app.models import Users

bp = Blueprint("auth", __name__, template_folder="templates")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # find user existence
        user = db.query(Users).filter_by(username=username).first()

        # validate password
        if user and user.check_password(password):
            login_user(user)

            return redirect(url_for("main.index"))

        
        flash("Invalid credentials", "warning")

    return render_template("login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))