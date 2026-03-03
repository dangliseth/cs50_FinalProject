from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from sqlalchemy import exc as mysql_errors

from app.db import db
from app.decorators import admin_required

from app.models import Students, Programs, Subjects, ProgramSubjects, StudentPrograms

bp = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@bp.route("/home")
@admin_required
def home():
    student_count = db.query(Students).count()
    program_count = db.query(Programs).count()
    subject_count = db.query(Subjects).count()

    all_subjects = db.query(Subjects).all()

    recent_students = db.query(Students).order_by(Students.id.desc()).limit(10).all()
    recent_enrolled_students = db.query(Students).join(StudentPrograms).filter(StudentPrograms.status == "Enrolled").order_by(Students.id.desc()).limit(10).all()

    return render_template("home.html", 
                           student_count=student_count, 
                           program_count=program_count, 
                           subject_count=subject_count, 
                           subjects=Subjects,
                           programs=Programs,
                           students=Students,
                           studentprograms=StudentPrograms,
                           recent_students=recent_students,
                           recent_enrolled_students=recent_enrolled_students,
                           all_subjects=all_subjects)

@bp.route("/student/<int:student_id>")
@admin_required
def view_student(student_id):
    student = db.query(Students).filter(Students.id == student_id).first()
    programs = db.query(Programs).join(StudentPrograms).filter(StudentPrograms.studentID == student_id).all()

    return render_template("view_student.html", student=student, Students=Students, programs=programs)

@bp.route("/subjects/add", methods=["GET", "POST"])
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
            flash(f"Added {name} successfully!", "success")
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

@bp.route("/programs/add", methods=["GET", "POST"])
@admin_required
def add_program():
    if request.method == "POST":
        try:
            code = request.form.get("code")
            title = request.form.get("title")
            name = request.form.get("name")
            
            # subject and subject requirement dictionary.
            subjectsAndRequirements = {}
            i= 0
            while True:
                # check if there are still subjects in form.
                subjectKey = f"subject-code-{i}"
                if subjectKey not in request.form:
                    break

                subject = request.form[subjectKey]

                if subject:
                    # if subject is not empty, assign requirement value: True or False.
                    requiredKey = f"required-{i}"
                    isRequired = requiredKey in request.form

                    subjectsAndRequirements[subject] = isRequired
                
                i += 1

            if not all([code, title, name, subjectsAndRequirements]):
                flash("Program code, title, and name cannot be empty.", "warning")
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({"success": False, "error": "Program code, title, and name cannot be empty.", "errorType": "warning"}), 400
                return redirect(url_for('admin.home'))

            program = db.query(Programs).where(Programs.code == code).first()

            if not program:
                newProgram = Programs(code=code, title=title, name=name)
                db.add(newProgram)

            for subject, isRequired in subjectsAndRequirements.items():
                if not db.query(Subjects).where(Subjects.code == subject).first():
                    return jsonify({"success": False, 
                                    "error": f"Subject: '{subject}' does not exist! Maybe add it first?",
                                    "errorType": "warning"
                                    }), 400
                
                newPS = ProgramSubjects(programCode=code, subjectCode=subject, required=isRequired)
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

@bp.route("/students/add", methods=["GET", "POST"])
@admin_required
def add_student():
    if request.method == "POST":
        programs = request.form.getlist("programNames")
        fname = str(request.form.get("firstName")).title()
        lname = str(request.form.get("lastName")).title()
        mname = str(request.form.get("middleName")).title()
        try:
            newStudent = Students(firstName=fname, lastName=lname, middleName=mname)
            db.add(newStudent)

            if programs:
                for prog_name in programs:
                    # 1. Find the Program object using the name from the form
                    program = db.query(Programs).filter_by(name=prog_name).first()
                    
                    if program:
                        # 2. Create the association object
                        # We set 'status' because it is nullable=False in your model
                        sp = StudentPrograms(status="Enrolled")
                        
                        # 3. Use the relationship! 
                        # Instead of manually setting programCode, we assign the object.
                        sp.programs = program
                        
                        # 4. Add to the student's list
                        newStudent.student_programs.append(sp)
            
            db.commit()
            flash(f"Added student {fname} {lname}", "success")
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": True, "redirect_url": url_for("admin.home")})
            return redirect(url_for("admin.home"))
        except mysql_errors.IntegrityError:
            db.rollback()
            flash("Database error! Duplicate Programs OR Student is already registered?", "danger")
        except Exception as e:
            db.rollback()
            flash(f"Error adding student: {e}", "danger")

    programNames = db.query(Programs.name).all()
    programNames = [program[0] for program in programNames]  # Extract names from tuples
    return render_template("add_student.html", studentprograms=StudentPrograms, programNames=programNames)
