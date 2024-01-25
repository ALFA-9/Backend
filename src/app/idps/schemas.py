from datetime import datetime

from pydantic import BaseModel, Field, validator


def datetime_format(dt: datetime):
    return dt.strftime("%d.%m.%Y")


class EmployeeDB(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str

    class Config:
        from_attributes = True


class IdpDB(BaseModel):
    id: int
    title: str
    status_idp: str
    date_start: datetime = Field(..., example="05.03.2024")
    date_end: datetime = Field(..., example="05.09.2024")
    employee: EmployeeDB
    director: EmployeeDB

    class Config:
        from_attributes = True
        json_encoders = {datetime: datetime_format}


class IdpCreate(BaseModel):
    title: str
    employee_id: int
    director_id: int
    date_end: datetime = Field(..., example="05.09.2024")

    @validator("date_end", pre=True)
    def parse_date_end(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value

    class Config:
        json_encoders = {datetime: datetime_format}


class IdpCreateDB(IdpCreate):
    date_start: datetime = Field(..., example="05.03.2024")
    id: int
