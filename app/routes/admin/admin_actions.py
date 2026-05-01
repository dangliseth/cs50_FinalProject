from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from sqlalchemy import exc as mysql_errors, or_

from app.db import db
from app.decorators import admin_required

from app.models import Students, Programs, Subjects, ProgramSubjects, StudentPrograms

from . import bp

# AJAX - Modal Function
@bp.route("/student/<int:student_id>/edit", methods=["POST"])
@admin_required
def edit_student(student_id):
    student = db.query(Students).get(student_id)

    if student:
        # Whitelist allowed fields for security
        allowed_fields = ["firstName", "lastName", "middleName"]

        try:
            updated = False
            for key, value in request.form.items():
                if key in allowed_fields:
                    # Convert empty strings to None (NULL in MySQL), otherwise use the value
                    val = value if value else None
                    setattr(student, key, val)
                    updated = True
            
            if not updated:
                raise ValueError("No valid input provided")
            
            db.commit()
            flash("Student updated successfully.", "success")
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": True, "redirect_url": request.referrer or url_for("admin.view_student", student_id=student_id)})
        except ValueError as e:
            db.rollback()
            flash(f"{e}.", "danger")
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": f"Database Error. {e}"}), 400
        except:
            db.rollback()
            flash(f"Error updating student {student.id}.", "danger")
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": "Database Error. Student was not updated!"}), 400

    return redirect(url_for("admin.view_student", student_id=student_id))

# AJAX - Modal Function
@bp.route("/student/<int:student_id>/enroll", methods=["POST"])
@admin_required
def enroll_student(student_id):
    program = request.form.get("enroll-program")
    
    try:
        existing_record = db.query(StudentPrograms).filter_by(studentID=student_id, programCode=program).first()
        if existing_record:
            existing_record.status = "Enrolled"
        else:
            enrollment = StudentPrograms(studentID=student_id, programCode=program, status="Enrolled")
            # db.merge() will INSERT if the primary key doesn't exist,
            # or UPDATE the existing record if it does.
            db.add(enrollment)
        db.commit()
        flash("Student enrolled successfully.", "success")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": True, "redirect_url": request.referrer or url_for("admin.view_student", student_id=student_id)})
    except Exception as e:
        db.rollback()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "error": str(e)}), 400

    return redirect(url_for("admin.view_student", student_id=student_id))

# AJAX - Modal Function
@bp.route("/student/<int:student_id>/drop-subjects", methods=["POST"])
@admin_required
def drop_subjects(student_id):
    programs = request.form.getlist("programs")

    try:
        if programs:
            for prog in programs:
                # 1. Find the existing record using the unique combination
                existing_record = db.query(StudentPrograms).filter_by(studentID=student_id, programCode=prog).first()
                
                if existing_record:
                    # 2. Update the status on the existing object
                    existing_record.status = "Dropped"
                else:
                    # 3. Fallback: If for some reason it doesn't exist, create it
                    new_drop = StudentPrograms(studentID=student_id, programCode=prog, status="Dropped")
                    db.add(new_drop)
            db.commit()
            
        flash(f"Dropped Subjects {programs}", "success")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": True, "redirect_url": request.referrer or url_for("admin.view_student", student_id=student_id)})
    except Exception as e:
        db.rollback()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "error": str(e)}), 400
    
    return redirect(url_for("admin.view_student", student_id=student_id))

# AJAX - Modal Function
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

# AJAX - Modal Function
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
            for key in request.form:
                if key.startswith("subject-code-"):
                    subject = request.form[key]
                    if subject:
                        # if subject is not empty, assign requirement value: True or False.
                        index = key.split("-")[-1]
                        requiredKey = f"required-{index}"
                        isRequired = requiredKey in request.form
                        subjectsAndRequirements[subject] = isRequired

            if not all([code, title, name, subjectsAndRequirements]):
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({"success": False, "error": "Program code, title, and name cannot be empty.", "errorType": "warning"}), 400
                return redirect(url_for('admin.home'))

            program = db.query(Programs).where(Programs.code == code).first()

            if not program:
                newProgram = Programs(code=code, title=title, name=name)
                db.add(newProgram)
            # If program exists, we might want to update it? If so, use db.merge(newProgram) instead.
            # For now, we leave the program details alone if it exists.

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
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": error_msg, "errorType": "danger"}), 400
            return redirect(url_for('admin.add_program'))
        except Exception as e:
            db.rollback()
            error_msg = f"An unexpected error occurred: {e}"
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
