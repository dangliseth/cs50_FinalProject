from flask import Blueprint, render_template, request, redirect, flash, url_for

from flask_login import login_user, logout_user, login_required, current_user
from app.db import db
from app.models import Users

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # find user existence
        user = db.query(Users).filter_by(username=username).first()

        # validate password
        if user and user.check_password(password):
            login_user(user)

        
        flash("Invalid credentials", "error")

    return render_template("auth/login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))