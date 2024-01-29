from dataclasses import dataclass
from datetime import datetime

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field, validator


def datetime_format(dt: datetime):
    return dt.strftime("%d.%m.%Y")


class IdpPut(BaseModel):
    status_idp: str


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


@dataclass
class RequestSchema:
    title: str = Form(...)
    letter: str = Form(...)
    director_id: int = Form(...)
    file: list[UploadFile] = File(None)
