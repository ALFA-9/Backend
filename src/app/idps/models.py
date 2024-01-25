from datetime import datetime

from pydantic import BaseModel


class EmployeeDB(BaseModel):
    id: int
    grade_id: int
    post_id: int
    department_id: int
    director_id: int
    person_id: int

    class Config:
        from_attributes = True


class DirectorDB(BaseModel):
    id: int

    class Config:
        from_attributes = True


class StatusIdpDB(BaseModel):
    title: str

    class Config:
        from_attributes = True


class IdpDB(BaseModel):
    id: int
    title: str
    employee: EmployeeDB
    director: DirectorDB
    status_idp: StatusIdpDB
    date_start: datetime
    date_end: datetime

    class Config:
        from_attributes = True


class IdpCreate(BaseModel):
    id: int
    title: str
    employee: int
    director: int
    status_idp: StatusIdpDB
    date_start: datetime = datetime.date.today()
    date_end: datetime
