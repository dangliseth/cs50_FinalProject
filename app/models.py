from typing import Optional

from sqlalchemy import ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Base(DeclarativeBase):
    pass


class Programs(Base):
    __tablename__ = 'programs'
    __table_args__ = (
        Index('id_UNIQUE', 'code', unique=True),
        Index('name_UNIQUE', 'name', unique=True)
    )

    code: Mapped[str] = mapped_column(String(45), primary_key=True)
    title: Mapped[str] = mapped_column(String(45), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    program_subjects: Mapped[list['ProgramSubjects']] = relationship('ProgramSubjects', back_populates='programs')
    student_programs: Mapped[list['StudentPrograms']] = relationship('StudentPrograms', back_populates='programs')


class Subjects(Base):
    __tablename__ = 'subjects'
    __table_args__ = (
        Index('id_UNIQUE', 'code', unique=True),
        Index('name_UNIQUE', 'name', unique=True)
    )

    code: Mapped[str] = mapped_column(String(45), primary_key=True)
    title: Mapped[str] = mapped_column(String(45), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    program_subjects: Mapped[list['ProgramSubjects']] = relationship('ProgramSubjects', back_populates='subjects')


class Users(UserMixin, Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('username_UNIQUE', 'username', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(254), nullable=False)
    role: Mapped[str] = mapped_column(String(15), nullable=False)

    students: Mapped[list['Students']] = relationship('Students', back_populates='user')

    # helper functions for password checking AND password setting.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


class ProgramSubjects(Base):
    __tablename__ = 'program_subjects'
    __table_args__ = (
        ForeignKeyConstraint(['programCode'], ['programs.code'], name='programCode_forSubjects'),
        ForeignKeyConstraint(['subjectCode'], ['subjects.code'], name='subjectCode'),
        Index('id_UNIQUE', 'id', unique=True),
        Index('programCode_subjectCode_UNIQUE', 'programCode', 'subjectCode', unique=True),
        Index('subjectCode_idx', 'subjectCode')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    programCode: Mapped[str] = mapped_column(String(45), nullable=False)
    subjectCode: Mapped[str] = mapped_column(String(45), nullable=False)
    required: Mapped[int] = mapped_column(TINYINT, nullable=False)

    programs: Mapped['Programs'] = relationship('Programs', back_populates='program_subjects')
    subjects: Mapped['Subjects'] = relationship('Subjects', back_populates='program_subjects')


class Students(Base):
    __tablename__ = 'students'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='users_studentsFK'),
        Index('id_UNIQUE', 'id', unique=True),
        Index('users_studentsFK_idx', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstName: Mapped[str] = mapped_column(String(45), nullable=False)
    lastName: Mapped[str] = mapped_column(String(45), nullable=False)
    middleName: Mapped[Optional[str]] = mapped_column(String(45))
    user_id: Mapped[Optional[int]] = mapped_column(Integer)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='students')
    student_programs: Mapped[list['StudentPrograms']] = relationship('StudentPrograms', back_populates='students')


class StudentPrograms(Base):
    __tablename__ = 'student_programs'
    __table_args__ = (
        ForeignKeyConstraint(['programCode'], ['programs.code'], name='programCode_forStudents'),
        ForeignKeyConstraint(['studentID'], ['students.id'], name='studentID'),
        Index('id_UNIQUE', 'id', unique=True),
        Index('programCode_idx', 'programCode'),
        Index('studentID_programCode_UNIQUE', 'studentID', 'programCode', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    studentID: Mapped[int] = mapped_column(Integer, nullable=False)
    programCode: Mapped[str] = mapped_column(String(45), nullable=False)
    status: Mapped[str] = mapped_column(String(45), nullable=False)

    programs: Mapped['Programs'] = relationship('Programs', back_populates='student_programs')
    students: Mapped['Students'] = relationship('Students', back_populates='student_programs')
