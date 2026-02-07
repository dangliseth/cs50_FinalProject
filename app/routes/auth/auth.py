from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify

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

        # success login.
        if user and user.check_password(password):
            login_user(user)

            # AJAX handling the login
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": True, "redirect_url": url_for("main.index")})

            # normal flask without AJAX
            return redirect(url_for("main.index"))

        # Failed Login. AJAX error handling
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
        
        # normal flask without AJAX
        flash("Invalid credentials", "warning")

    return render_template("login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))