from dataclasses import dataclass
from datetime import date, datetime

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field, validator

from app.tasks.schemas import (CurrentTask, TaskForIdpCreate,
                               TaskForIdpCreateDB, TaskWithComments)


def datetime_format(dt: datetime):
    return dt.strftime("%d.%m.%Y")


class IdpPut(BaseModel):
    status_idp: str


class IdpForEmployee(BaseModel):
    id: int
    title: str
    status_idp: str
    director: str
    date_start: datetime = Field(..., examples=["13.05.2024"])
    date_end: datetime = Field(..., examples=["13.11.2024"])

    class Config:
        json_encoders = {datetime: datetime_format}


class IdpList(BaseModel):
    id: int
    title: str
    status_idp: str
    date_start: datetime = Field(..., examples=["13.05.2024"])
    date_end: datetime = Field(..., examples=["13.11.2024"])
    employee_id: int
    director_id: int

    class Config:
        json_encoders = {datetime: datetime_format}


class EmployeeDB(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str

    class Config:
        from_attributes = True


class IdpDB(IdpList):
    employee: EmployeeDB
    director: EmployeeDB

    class Config:
        from_attributes = True
        json_encoders = {datetime: datetime_format}


class IdpCreate(BaseModel):
    title: str
    employee_id: int
    tasks: list[TaskForIdpCreate]
    date_end: datetime = Field(..., examples=["13.11.2024"])

    @validator("date_end", pre=True)
    def parse_date_end(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value

    class Config:
        json_encoders = {datetime: datetime_format}


class IdpCreateDB(IdpCreate):
    date_start: datetime = Field(..., examples=["13.05.2024"])
    status_idp: str
    id: int
    tasks: list[TaskForIdpCreateDB]

    class Config:
        from_attributes = True


class IdpRetrieve(BaseModel):
    title: str
    employee_id: int
    director_id: int
    status_idp: str
    tasks: list[TaskWithComments]

    class Config:
        populate_by_name = True
        from_attributes = True


class IdpWithCurrentTask(BaseModel):
    id: int
    director: str
    title: str
    status_idp: str
    progress: float = Field(validation_alias="tasks")
    current_task: CurrentTask | None = Field(validation_alias="tasks")

    @validator("director", pre=True)
    def get_director_full_name(cls, v, values) -> str:
        return f"{v.last_name} {v.first_name} {v.patronymic}"

    @validator("current_task", pre=True)
    def get_current_task(cls, v, values) -> CurrentTask | None:
        for task in v:
            data = task.__dict__
            if data["date_start"] <= date.today() < data["date_end"]:
                return CurrentTask(**data)
        return None

    @validator("progress", pre=True)
    def get_progress(cls, v, values) -> float:
        done_count = 0
        not_cancelled_count = 0
        for task in v:
            data = task.__dict__
            if data["status_progress"].value != "cancelled":
                not_cancelled_count += 1
                if data["status_progress"].value == "done":
                    done_count += 1
        return (done_count / not_cancelled_count) * 100


@dataclass
class RequestSchema:
    title: str = Form(...)
    letter: str = Form(...)
    director_id: int = Form(...)
    files: list[UploadFile] = File(None)
