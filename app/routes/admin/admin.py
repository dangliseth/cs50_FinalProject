from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from sqlalchemy import exc as mysql_errors

from app.db import db
from app.decorators import admin_required

from app.models import Students, Programs, Subjects, ProgramSubjects

bp = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@bp.route("/home")
@admin_required
def home():
    student_count = db.query(Students).count()
    program_count = db.query(Programs).count()
    subject_count = db.query(Subjects).count()

    all_subjects = db.query(Subjects).all()

    recent_students = db.query(Students).order_by(Students.id.desc()).limit(10).all()

    return render_template("home.html", 
                           student_count=student_count, 
                           program_count=program_count, 
                           subject_count=subject_count, 
                           subjects=Subjects,
                           programs=Programs,
                           students=Students,
                           recent_students=recent_students,
                           all_subjects=all_subjects)

@bp.route("/subject/add", methods=["GET", "POST"])
@admin_required
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

@bp.route("/program/add", methods=["GET", "POST"])
@admin_required
def add_program():
    if request.method == "POST":
        try:
            code = request.form.get("code")
            title = request.form.get("title")
            name = request.form.get("name")
            required = bool(request.form.get("required"))

            # subject-code-i iteration from request.form
            subjectCodes = []
            for key in request.form:
                if key.startswith("subject-code"):
                    subjectCodes.append(request.form[key])

            if not all([code, title, name, subjectCodes]):
                flash("Program code, title, and name cannot be empty.", "warning")
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({"success": False, "error": "Program code, title, and name cannot be empty.", "errorType": "warning"}), 400
                return redirect(url_for('admin.home'))

            program = db.query(Programs).where(Programs.code == code).first()

            if not program:
                newProgram = Programs(code=code, title=title, name=name)
                db.add(newProgram)

            for subject in subjectCodes:
                if not db.query(Subjects).where(Subjects.code == subject).first():
                    return jsonify({"success": False, 
                                    "error": f"Subject: '{subject}' does not exist! Maybe add it first?",
                                    "errorType": "warning"
                                    }), 400
                
                newPS = ProgramSubjects(programCode=code, subjectCode=subject, required=required)
                db.add(newPS)
            
            db.commit()

            flash(f"Successfully added program '{title}'.", "success")
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": True, "redirect_url": url_for("admin.home")})
            
            return redirect(url_for("admin.home"))
        except mysql_errors.IntegrityError:
            db.rollback()
            error_msg = "Database error: A program with this code might already exist, or a duplicate subject."
            flash(error_msg, "danger")
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": error_msg, "errorType": "danger"}), 400
            return redirect(url_for('admin.add_program'))
        except Exception as e:
            db.rollback()
            error_msg = f"An unexpected error occurred: {e}"
            flash(error_msg, "danger")
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": str(e), "errorType": "danger"}), 500
            return redirect(url_for('admin.add_program'))

    return render_template("home.html")
