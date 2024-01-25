from enum import Enum as PythonEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


# Создаем таблицы(что-то вроде моделей в Django)
class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    grade_id = Column(
        Integer, ForeignKey("grade.id", ondelete="SET NULL"), nullable=True
    )
    post_id = Column(
        Integer, ForeignKey("post.id", ondelete="SET NULL"), nullable=True
    )
    department_id = Column(
        Integer, ForeignKey("department.id", ondelete="CASCADE"), nullable=True
    )
    director_id = Column(
        Integer, ForeignKey("employee.id", ondelete="SET NULL"), nullable=True
    )
    first_name = Column(String(80))
    last_name = Column(String(80))
    patronymic = Column(String(80))
    email = Column(String(100))
    phone = Column(String(20))

    grade = relationship("Grade", back_populates="employee", lazy="joined")
    post = relationship("Post", back_populates="employee", lazy="joined")
    department = relationship(
        "Department",
        back_populates="employee",
        lazy="joined",
    )
    employees = relationship("Employee", lazy="joined", join_depth=3)
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


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    body_comment = Column(String(200))
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"))
    employee_id = Column(
        Integer, ForeignKey("employee.id", ondelete="CASCADE")
    )

    employee = relationship(
        "Employee", back_populates="comment", lazy="joined"
    )
    task = relationship("Task", back_populates="comment", lazy="joined")


class Task(Base):
    class StatusProgress(PythonEnum):
        IN_WORK = "in_work"
        DONE = "done"

    class StatusAccept(PythonEnum):
        ACCEPTED = "accepted"
        NOT_ACCEPTED = "not_accepted"
        CANCELED = "canceled"

    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    idp_id = Column(Integer, ForeignKey("idp.id", ondelete="CASCADE"))
    status_progress = Column(
        Enum(StatusProgress), default=StatusProgress.IN_WORK
    )
    status_accept = Column(Enum(StatusAccept), nullable=True, default=None)
    task_type_id = Column(
        Integer, ForeignKey("taskType.id", ondelete="SET NULL"), nullable=True
    )
    control_id = Column(
        Integer,
        ForeignKey("taskControl.id", ondelete="SET NULL"),
        nullable=True,
    )

    idp = relationship("Idp", back_populates="task", lazy="joined")
    task_type = relationship("TaskType", back_populates="task", lazy="joined")
    task_control = relationship(
        "TaskControl",
        back_populates="task",
        lazy="joined",
    )
    comment = relationship("Comment", back_populates="task", lazy="joined")


class Idp(Base):
    class StatusIdp(PythonEnum):
        IN_WORK = "in_work"
        NOT_COMPLETED = "not_completed"
        DONE = "done"
        CANCELED = "canceled"

    __tablename__ = "idp"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    employee_id = Column(
        Integer, ForeignKey("employee.id", ondelete="CASCADE")
    )
    director_id = Column(
        Integer, ForeignKey("employee.id", ondelete="SET NULL"), nullable=True
    )
    status_idp_id = Column(Enum(StatusIdp), default=StatusIdp.IN_WORK)
    date_start = Column(DateTime, default=func.now(), nullable=False)
    date_end = Column(DateTime)

    employee = relationship(
        "Employee",
        backref="idp_emp",
        lazy="joined",
        foreign_keys=[employee_id],
        cascade="all, delete",
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
        "Task",
        back_populates="task_status_progress",
        lazy="joined",
    )


class TaskStatusAccept(Base):
    __tablename__ = "taskStatusAccept"
    id = Column(Integer, primary_key=True)
    status = Column(String(50))

    task = relationship(
        "Task",
        back_populates="task_status_accept",
        lazy="joined",
    )


class TaskControl(Base):
    __tablename__ = "taskControl"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    task = relationship("Task", back_populates="task_control", lazy="joined")
