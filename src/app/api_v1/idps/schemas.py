from dataclasses import dataclass
from datetime import date, datetime

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field, field_validator, ConfigDict

from app.api_v1.tasks.schemas import (CurrentTask, TaskForIdpCreate,
                                      TaskForIdpCreateDB, TaskWithComments)


def datetime_format(dt: datetime):
    return dt.strftime("%d.%m.%Y")


class IdpPatch(BaseModel):
    status_idp: str


class IdpForEmployee(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: datetime_format})

    id: int
    title: str
    status_idp: str
    director: str
    date_start: datetime = Field(..., examples=["13.05.2024"])
    date_end: datetime = Field(..., examples=["13.11.2024"])


class IdpList(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: datetime_format})

    id: int
    title: str
    status_idp: str
    date_start: datetime = Field(..., examples=["13.05.2024"])
    date_end: datetime = Field(..., examples=["13.11.2024"])
    employee_id: int
    director_id: int


class EmployeeDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    patronymic: str


class IdpDB(IdpList):
    model_config = ConfigDict(json_encoders={datetime: datetime_format}, from_attributes = True)

    employee: EmployeeDB
    director: EmployeeDB


class IdpCreate(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: datetime_format})

    title: str
    employee_id: int
    tasks: list[TaskForIdpCreate]
    date_end: datetime = Field(..., examples=["13.11.2024"])

    @field_validator("date_end", mode="before")
    def parse_date_end(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value


class IdpCreateDB(IdpCreate):
    model_config = ConfigDict(from_attributes = True)

    date_start: datetime = Field(..., examples=["13.05.2024"])
    status_idp: str
    id: int
    tasks: list[TaskForIdpCreateDB]


class IdpRetrieve(BaseModel):
    model_config = ConfigDict(from_attributes = True, populate_by_name=True)

    title: str
    employee_id: int
    director_id: int
    status_idp: str
    tasks: list[TaskWithComments]


class IdpWithCurrentTask(BaseModel):
    id: int
    director: str
    title: str
    status_idp: str
    progress: float = Field(validation_alias="tasks")
    current_task: CurrentTask | None = Field(validation_alias="tasks")

    @field_validator("director", mode="before")
    def get_director_full_name(cls, v, values) -> str:
        return f"{v.last_name} {v.first_name} {v.patronymic}"

    @field_validator("current_task", mode="before")
    def get_current_task(cls, v, values) -> CurrentTask | None:
        for task in v:
            data = task.__dict__
            if data["date_start"] <= date.today() < data["date_end"]:
                return CurrentTask(**data)
        return None

    @field_validator("progress", mode="before")
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
    file: UploadFile = File(None)
