from enum import Enum as PythonEnum

from sqlalchemy import (Boolean, Column, Date, DateTime, Enum, ForeignKey,
                        Integer, String, Text)
from sqlalchemy.orm import backref, relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    grade_id = Column(
        Integer,
        ForeignKey("grade.id", ondelete="SET NULL"),
        nullable=True,
    )
    post_id = Column(
        Integer,
        ForeignKey("post.id", ondelete="SET NULL"),
        nullable=True,
    )
    department_id = Column(
        Integer,
        ForeignKey("department.id", ondelete="SET NULL"),
        nullable=True,
    )
    director_id = Column(
        Integer,
        ForeignKey("employee.id", ondelete="SET NULL"),
        nullable=True,
    )
    first_name = Column(String(80))
    last_name = Column(String(80))
    patronymic = Column(String(80))
    email = Column(String(100))
    phone = Column(String(20))
    last_request = Column(DateTime, nullable=True)

    grade = relationship("Grade", back_populates="employee", lazy="joined")
    post = relationship("Post", back_populates="employee", lazy="joined")
    department = relationship(
        "Department",
        back_populates="employee",
        lazy="joined",
    )
    employees = relationship(
        "Employee",
        lazy="joined",
        backref=backref("director", uselist=False, remote_side=[id], lazy="joined"),
    )
    comment = relationship("Comment", back_populates="employee", lazy="joined")

    def __str__(self):
        return f"{self.id} {self.last_name} {self.first_name} {self.patronymic}"


class Grade(Base):
    __tablename__ = "grade"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    employee = relationship("Employee", back_populates="grade", lazy="joined")

    def __str__(self):
        return self.title


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    employee = relationship("Employee", back_populates="post", lazy="joined")

    def __str__(self):
        return self.title


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    employee = relationship("Employee", back_populates="department", lazy="joined")

    def __str__(self):
        return self.title


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    body_comment = Column(String(200))
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"))
    employee_id = Column(Integer, ForeignKey("employee.id", ondelete="CASCADE"))
    pub_date = Column(DateTime, server_default=func.now(), default=func.now())

    employee = relationship("Employee", back_populates="comment", lazy="joined")
    task = relationship("Task", back_populates="comment", lazy="joined")

    def __str__(self):
        return self.body_comment


class Task(Base):
    class StatusProgress(PythonEnum):
        in_work = "in_work"
        done = "done"
        not_completed = "not_completed"
        cancelled = "cancelled"

    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text)
    idp_id = Column(Integer, ForeignKey("idp.id", ondelete="CASCADE"))
    status_progress = Column(Enum(StatusProgress), default=StatusProgress.in_work)
    is_completed = Column(Boolean, default=False)
    date_start = Column(Date)
    date_end = Column(Date)
    type_id = Column(
        Integer,
        ForeignKey("type.id", ondelete="SET NULL"),
        nullable=True,
    )
    control_id = Column(
        Integer,
        ForeignKey("control.id", ondelete="SET NULL"),
        nullable=True,
    )

    idp = relationship("Idp", back_populates="tasks", lazy="joined")
    task_type = relationship("TaskType", back_populates="task", lazy="joined")
    task_control = relationship(
        "TaskControl",
        back_populates="task",
        lazy="joined",
    )
    comment = relationship("Comment", back_populates="task", lazy="joined")

    def __str__(self):
        return self.name


class Idp(Base):
    class StatusIdp(PythonEnum):
        in_work = "in_work"
        not_completed = "not_completed"
        done = "done"
        cancelled = "cancelled"

    __tablename__ = "idp"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    employee_id = Column(
        Integer,
        ForeignKey("employee.id", ondelete="CASCADE"),
    )
    director_id = Column(
        Integer,
        ForeignKey("employee.id"),
        nullable=True,
    )
    status_idp = Column(Enum(StatusIdp), default=StatusIdp.in_work)
    date_start = Column(Date, server_default=func.now(), default=func.now())

    employee = relationship(
        "Employee",
        backref="idp_emp",
        lazy="joined",
        foreign_keys=[employee_id],
    )
    director = relationship(
        "Employee",
        backref="idp_dir",
        lazy="joined",
        foreign_keys=[director_id],
    )
    tasks = relationship("Task", back_populates="idp", lazy="joined")

    def __str__(self):
        return self.title


class TaskType(Base):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    task = relationship("Task", back_populates="task_type", lazy="joined")

    def __str__(self):
        return self.name


class TaskControl(Base):
    __tablename__ = "control"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    task = relationship("Task", back_populates="task_control", lazy="joined")

    def __str__(self):
        return self.title
