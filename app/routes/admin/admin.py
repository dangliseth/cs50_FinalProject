from flask import Blueprint, render_template, request

from app.db import db

from app.models import Students, Programs, Subjects

bp = Blueprint("admin", __name__, template_folder="templates")

@bp.route("/home")
def home():
    student_count = db.query(Students).count()
    program_count = db.query(Programs).count()
    subject_count = db.query(Subjects).count()

    return render_template("home.html", student_count=student_count, program_count=program_count, subject_count=subject_count)

@bp.route("/subject/add", methods=["GET", "POST"])
def add_subject():
    if request.method == "POST":
        code = request.form["code"]
        title = request.form["title"]
        name = request.form["name"]

    return render_template("add_subject.html", model=Subjects)