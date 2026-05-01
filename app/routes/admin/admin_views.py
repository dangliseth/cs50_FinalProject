from flask import render_template, request, jsonify, redirect, url_for, flash
from sqlalchemy import exc as mysql_errors, or_

from app.db import db
from app.decorators import admin_required
from . import bp

from app.models import Students, Programs, Subjects, ProgramSubjects, StudentPrograms


# Includes Modal Functions
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

# Includes Modal Functions
@bp.route("/student/<int:student_id>")
@admin_required
def view_student(student_id):
    student = db.query(Students).filter(Students.id == student_id).first()
    
    # Query Programs AND the status column, then manually attach status to the Program objects
    results = db.query(Programs, StudentPrograms.status).join(StudentPrograms).filter(StudentPrograms.studentID == student_id).all()
    programs = []
    for prog, status in results:
        prog.status = status
        programs.append(prog)

    return render_template("view_student.html", student=student, Students=Students, programs=programs)

@bp.route("/students")
@admin_required
def view_students_table():
    stmt = db.query(Students).join(StudentPrograms)

    search_query = request.args.get("q")
    status = request.args.get("status")

    columns = [col for col in Students.__table__.columns if col.name.lower() != "user_id"]
    columns.append(StudentPrograms.status)

    if status:
        stmt = stmt.filter(StudentPrograms.status == status)

    if search_query:
        fltr = [col.ilike(f"%{search_query}%") for col in columns]
        stmt = stmt.filter(or_(*fltr))

    all_students = stmt.distinct().all()

    return render_template("view_students_table.html", 
                           Students=Students, 
                           all_students=all_students, 
                           columns=columns, 
                           status=status,
                           search_query=search_query)

@bp.route("/subjects")
@admin_required
def view_subjects_table():
    # Eagerly load the relationships to prevent N+1 queries in the template
    stmt = db.query(Subjects)

    columns = [col for col in Subjects.__table__.columns]
    columns.append(Programs.code)
    columns.append(ProgramSubjects.required)

    search_query = request.args.get("q")

    if search_query:
        # Only filter by string-based columns to avoid errors
        searchable_cols = [
            Subjects.code,
            Subjects.title,
            Subjects.name
        ]
        fltr = [col.ilike(f"%{search_query}%") for col in searchable_cols]
        stmt = stmt.filter(or_(*fltr))

    subjects = stmt.distinct().all()

    return render_template("view_subjects_table.html", subjects=subjects, columns=columns, search_query=search_query)