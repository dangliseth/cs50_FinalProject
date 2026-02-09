from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from sqlalchemy import exc as mysql_errors

from app.db import db

from app.models import Students, Programs, Subjects

bp = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@bp.route("/home")
def home():
    student_count = db.query(Students).count()
    program_count = db.query(Programs).count()
    subject_count = db.query(Subjects).count()

    return render_template("home.html", student_count=student_count, program_count=program_count, subject_count=subject_count, model=Subjects)

@bp.route("/subject/add", methods=["GET", "POST"])
def add_subject():
    if request.method == "POST":
        try:
            code = request.form["code"]
            title = request.form["title"]
            name = request.form["name"]

            new_subject = Subjects(code=code, title=title, name=name)

            db.add(new_subject)
            db.commit()

            #js AJAX redirect
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": True, "redirect_url": url_for("admin.home")})
            
            return redirect(url_for("admin.home"))
        except mysql_errors.IntegrityError as e:
            db.rollback()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": "Database error! PROBABLY a duplicate."}), 400
        except Exception as e:
            db.rollback()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": str(e)}), 400
            

    return render_template("add_subject.html", model=Subjects)