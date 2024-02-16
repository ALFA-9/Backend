from dataclasses import dataclass
from datetime import date, datetime

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.api_v1.tasks.schemas import (CurrentTask, TaskForIdpCreate,
                                      TaskForIdpCreateDB, TaskWithComments)
from app.database.models import Idp


def datetime_format(dt: datetime):
    return dt.strftime("%d.%m.%Y")


class IdpPatch(BaseModel):
    status_idp: Idp.StatusIdp


class IdpCreate(BaseModel):
    title: str = Field(examples=["Learn Java"])
    employee_id: int = Field(examples=[22099])
    tasks: list[TaskForIdpCreate]


class IdpCreateDB(IdpCreate):
    model_config = ConfigDict(from_attributes=True)

    status_idp: Idp.StatusIdp
    id: int = Field(examples=[22002])
    tasks: list[TaskForIdpCreateDB]


class IdpRetrieve(IdpCreateDB):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int = Field(exclude=True)
    director_id: int = Field(examples=[22001])
    tasks: list[TaskWithComments]


class IdpWithCurrentTask(BaseModel):
    id: int = Field(examples=[22002])
    director: str = Field(examples=["Johnov John Johnovich"])
    title: str = Field(examples=["Learn Kotlin"])
    status_idp: Idp.StatusIdp
    progress: float = Field(validation_alias="tasks", examples=[66])
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
