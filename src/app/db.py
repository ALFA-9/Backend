import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine, ForeignKey)
from sqlalchemy.sql import func
from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Создаем таблицы(что-то вроде моделей в Django)
employees = Table(
    'employee',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('grade_id', Integer, ForeignKey('grade.id')),
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('departament_id', Integer, ForeignKey('departament.id')),
    Column('director_id', Integer, ForeignKey('director.id')),
    Column('person_id', Integer, ForeignKey('person.id')),
)

grades = Table(
    'grade',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(200)),
)

posts = Table(
    'post',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(200)),
)

departaments = Table(
    'departament',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(200)),
)

directors = Table(
    'director',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('person_id', Integer, ForeignKey('person.id')),
)

persons = Table(
    'person',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String(80)),
    Column('last_name', String(80)),
    Column('patronymic', String(80)),
    Column('email', String(100)),
    Column('phone', String(20)),
)

requests = Table(
    'request',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100)),
    Column('letter', String(1000)),
    Column('director_id', Integer, ForeignKey('director.id')),
    Column('employee_id', Integer, ForeignKey('employee.id')),
)

comments = Table(
    'comment',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('bodyComment', String(200)),
    Column('task_id', Integer, ForeignKey('task.id')),
    Column('employee_id', Integer, ForeignKey('employee.id')),
)

tasks = Table(
    'task',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('idp_id', Integer, ForeignKey('idp.id')),
    Column('taskType_id', Integer, ForeignKey('taskType.id')),
    Column('statusProgress_id', Integer, ForeignKey('taskStatusProgress.id')),
    Column('statusAccept_id', Integer, ForeignKey('taskStatusAccept.id')),
    Column('control_id', Integer, ForeignKey('taskControl.id')),
)

idps = Table(
    'idp',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100)),
    Column('employee_id', Integer, ForeignKey('employee.id')),
    Column('director_id', Integer, ForeignKey('director.id')),
    Column('statusIdp_id', Integer, ForeignKey('statusIdp.id')),
    Column('date_start', DateTime, default=func.now(), nullable=False),
    Column('date_end', DateTime)
)

statuses_idp = Table(
    'statusIdp',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(50)),
)

task_types = Table(
    'taskType',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
)

task_statuses_progress = Table(
    'taskStatusProgress',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('status', String(50)),
)

task_statuses_accept = Table(
    'taskStatusAccept',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('status', String(50)),
)

task_controls = Table(
    'taskControl',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100)),
)


# databases query builder
database = Database(DATABASE_URL)
