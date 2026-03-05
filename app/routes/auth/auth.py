from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from urllib.parse import urlparse

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

            next_page = request.args.get("next")
            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("main.index")

            # AJAX handling the login
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": True, "redirect_url": next_page})

            # normal flask without AJAX
            return redirect(next_page)

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