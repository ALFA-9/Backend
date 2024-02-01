from pydantic import BaseModel, EmailStr

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
    post: Post
    grade: Grade
    department: Department

    class Config:
        from_attributes = True
        json_encoders = {
            Post: lambda v: v.title,
            Grade: lambda v: v.title,
            Department: lambda v: v.title,
        }


class EmployeeChild(EmployeeLastChild):
    employees: list[EmployeeLastChild]

    class Config:
        from_attributes = True


class EmployeeWithIdps(EmployeeLastChild):
    idps: list[IdpForEmployee] | None

    class Config:
        from_attributes = True
