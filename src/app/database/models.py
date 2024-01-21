from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


# Создаем таблицы(что-то вроде моделей в Django)
class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    grade_id = Column(Integer, ForeignKey("grade.id"))
    post_id = Column(Integer, ForeignKey("post.id"))
    department_id = Column(Integer, ForeignKey("department.id"))
    director_id = Column(Integer, ForeignKey("employee.id"))
    first_name = Column(String(80))
    last_name = Column(String(80))
    patronymic = Column(String(80))
    email = Column(String(100))
    phone = Column(String(20))

    grade = relationship("Grade", back_populates="employee", lazy="joined")
    post = relationship("Post", back_populates="employee", lazy="joined")
    department = relationship(
        "Department", back_populates="employee", lazy="joined"
    )
    employees = relationship("Employee", lazy="joined")
    comment = relationship("Comment", back_populates="employee", lazy="joined")


class Grade(Base):
    __tablename__ = "grade"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    employee = relationship("Employee", back_populates="grade", lazy="joined")


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    employee = relationship("Employee", back_populates="post", lazy="joined")


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    employee = relationship(
        "Employee", back_populates="department", lazy="joined"
    )


class Request(Base):
    __tablename__ = "request"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    letter = Column(String(1000))
    director_id = Column(Integer, ForeignKey("employee.id"))
    employee_id = Column(Integer, ForeignKey("employee.id"))

    employee = relationship(
        "Employee",
        backref="request_emp",
        lazy="joined",
        foreign_keys=[employee_id],
    )
    director = relationship(
        "Employee",
        backref="request_dir",
        lazy="joined",
        foreign_keys=[director_id],
    )


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    body_comment = Column(String(200))
    task_id = Column(Integer, ForeignKey("task.id"))
    employee_id = Column(Integer, ForeignKey("employee.id"))

    employee = relationship(
        "Employee", back_populates="comment", lazy="joined"
    )
    task = relationship("Task", back_populates="comment", lazy="joined")


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    idp_id = Column(Integer, ForeignKey("idp.id"))
    task_type_id = Column(Integer, ForeignKey("taskType.id"))
    status_progress_id = Column(Integer, ForeignKey("taskStatusProgress.id"))
    status_accept_id = Column(Integer, ForeignKey("taskStatusAccept.id"))
    control_id = Column(Integer, ForeignKey("taskControl.id"))

    idp = relationship("Idp", back_populates="task", lazy="joined")
    task_type = relationship("TaskType", back_populates="task", lazy="joined")
    task_status_progress = relationship(
        "TaskStatusProgress", back_populates="task", lazy="joined"
    )
    task_status_accept = relationship(
        "TaskStatusAccept", back_populates="task", lazy="joined"
    )
    task_control = relationship(
        "TaskControl", back_populates="task", lazy="joined"
    )
    comment = relationship("Comment", back_populates="task", lazy="joined")


class Idp(Base):
    __tablename__ = "idp"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    employee_id = Column(Integer, ForeignKey("employee.id"))
    director_id = Column(Integer, ForeignKey("employee.id"))
    status_idp_id = Column(Integer, ForeignKey("statusIdp.id"))
    date_start = Column(DateTime, default=func.now(), nullable=False)
    date_end = Column(DateTime)

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
    status_idp = relationship("StatusIdp", back_populates="idp", lazy="joined")
    task = relationship("Task", back_populates="idp", lazy="joined")


class StatusIdp(Base):
    __tablename__ = "statusIdp"
    id = Column(Integer, primary_key=True)
    title = Column(String(50))

    idp = relationship("Idp", back_populates="status_idp", lazy="joined")


class TaskType(Base):
    __tablename__ = "taskType"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    task = relationship("Task", back_populates="task_type", lazy="joined")


class TaskStatusProgress(Base):
    __tablename__ = "taskStatusProgress"
    id = Column(Integer, primary_key=True)
    status = Column(String(50))

    task = relationship(
        "Task", back_populates="task_status_progress", lazy="joined"
    )


class TaskStatusAccept(Base):
    __tablename__ = "taskStatusAccept"
    id = Column(Integer, primary_key=True)
    status = Column(String(50))

    task = relationship(
        "Task", back_populates="task_status_accept", lazy="joined"
    )


class TaskControl(Base):
    __tablename__ = "taskControl"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    task = relationship("Task", back_populates="task_control", lazy="joined")
