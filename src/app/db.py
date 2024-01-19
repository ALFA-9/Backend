import os

from sqlalchemy import (Column, DateTime, Integer, String,
                        create_engine, ForeignKey)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Создаем таблицы(что-то вроде моделей в Django)
class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    grade_id = Column(Integer, ForeignKey('grade.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    department_id = Column(Integer, ForeignKey('department.id'))
    director_id = Column(Integer, ForeignKey('director.id'))
    person_id = Column(Integer, ForeignKey('person.id'))

    grade = relationship("Grade", back_populates="employee")
    post = relationship("Post", back_populates="employee")
    department = relationship("Department", back_populates="employee")
    director = relationship("Director", back_populates="employee")
    person = relationship("Person", back_populates="employee")
    request = relationship("Request", back_populates="employee")
    comment = relationship("Comment", back_populates="employee")
    idp = relationship("Idp", back_populates="employee")


class Grade(Base):
    __tablename__ = 'grade'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    employee = relationship("Employee", back_populates="grade")


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    employee = relationship("Employee", back_populates="post")


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    employee = relationship("Employee", back_populates="department")


class Director(Base):
    __tablename__ = 'director'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))

    employee = relationship("Employee", back_populates="director")
    person = relationship("Person", back_populates="director")
    request = relationship("Request", back_populates="director")
    idp = relationship("Idp", back_populates="director")


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(80))
    last_name = Column(String(80))
    patronymic = Column(String(80))
    email = Column(String(100))
    phone = Column(String(20))

    employee = relationship("Employee", back_populates="person")
    director = relationship("Director", back_populates="person")


class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    letter = Column(String(1000))
    director_id = Column(Integer, ForeignKey('director.id'))
    employee_id = Column(Integer, ForeignKey('employee.id'))

    employee = relationship("Employee", back_populates="request")
    director = relationship("Director", back_populates="request")


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    body_comment = Column(String(200))
    task_id = Column(Integer, ForeignKey('task.id'))
    employee_id = Column(Integer, ForeignKey('employee.id'))

    employee = relationship("Employee", back_populates="comment")
    task = relationship("Task", back_populates="comment")


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    idp_id = Column(Integer, ForeignKey('idp.id'))
    task_type_id = Column(Integer, ForeignKey('taskType.id'))
    status_progress_id = Column(Integer, ForeignKey('taskStatusProgress.id'))
    status_accept_id = Column(Integer, ForeignKey('taskStatusAccept.id'))
    control_id = Column(Integer, ForeignKey('taskControl.id'))

    idp = relationship("Idp", back_populates="task")
    task_type = relationship("TaskType", back_populates="task")
    task_status_progress = relationship("TaskStatusProgress",
                                        back_populates="task")
    task_status_accept = relationship("TaskStatusAccept",
                                      back_populates="task")
    task_control = relationship("TaskControl", back_populates="task")
    comment = relationship("Comment", back_populates="task")


class Idp(Base):
    __tablename__ = 'idp'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    employee_id = Column(Integer, ForeignKey('employee.id'))
    director_id = Column(Integer, ForeignKey('director.id'))
    status_idp_id = Column(Integer, ForeignKey('statusIdp.id'))
    date_start = Column(DateTime, default=func.now(), nullable=False)
    date_end = Column(DateTime)

    employee = relationship("Employee", back_populates="idp")
    director = relationship("Director", back_populates="idp")
    status_idp = relationship("StatusIdp", back_populates="idp")
    task = relationship("Task", back_populates="idp")


class StatusIdp(Base):
    __tablename__ = 'statusIdp'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))

    idp = relationship("Idp", back_populates="status_idp")


class TaskType(Base):
    __tablename__ = 'taskType'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    task = relationship("Task", back_populates="task_type")


class TaskStatusProgress(Base):
    __tablename__ = 'taskStatusProgress'
    id = Column(Integer, primary_key=True)
    status = Column(String(50))

    task = relationship("Task", back_populates="task_status_progress")


class TaskStatusAccept(Base):
    __tablename__ = 'taskStatusAccept'
    id = Column(Integer, primary_key=True)
    status = Column(String(50))

    task = relationship("Task", back_populates="task_status_accept")


class TaskControl(Base):
    __tablename__ = 'taskControl'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    task = relationship("Task", back_populates="task_control")


# databases query builder
database = Database(DATABASE_URL)
