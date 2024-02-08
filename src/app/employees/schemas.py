from pydantic import BaseModel, EmailStr, Field, validator

from app.constants import MAX_RECURSION
from app.idps.schemas import IdpForEmployee


class AuthEmployeeSchema(BaseModel):
    email: EmailStr


class Grade(BaseModel):
    title: str


class Post(BaseModel):
    title: str


class Department(BaseModel):
    title: str


class EmployeeLastChild(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str
    post: str = Field(examples=["Director"])
    # image:
    # status_idp:

    @validator("post", pre=True, always=True)
    def get_post(cls, v, values) -> str:
        return v.title

    class Config:
        from_attributes = True
        json_encoders = {
            Post: lambda v: v.title,
            Grade: lambda v: v.title,
            Department: lambda v: v.title,
        }


class EmployeeChild(EmployeeLastChild):
    max_recursion: int = Field(MAX_RECURSION, exclude=True)
    employees: list["EmployeeChild"]

    @validator("employees", pre=True)
    def get_employees(cls, value, values):
        if values["max_recursion"] > 1:
            print([child.__dict__ for child in value])
            return [
                EmployeeChild(
                    **child.__dict__, max_recursion=values["max_recursion"] - 1
                )
                for child in value
            ]
        else:
            return []

    class Config:
        from_attributes = True


class EmployeeWithIdps(EmployeeLastChild):
    idps: list[IdpForEmployee] | None

    class Config:
        from_attributes = True
