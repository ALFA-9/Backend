from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class GradeDB(BaseModel):
    title: str

    class Config:
        from_attributes = True


class EmployeeLastChild(BaseModel):
    id: int
    director_id: int
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    phone: PhoneNumber

    class Config:
        from_attributes = True


class EmployeeChild(BaseModel):
    id: int
    director_id: int
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    phone: PhoneNumber
    employees: list[EmployeeLastChild]

    class Config:
        from_attributes = True


class EmployeeSchema(BaseModel):
    grade_id: int
    post_id: int
    department_id: int
    director_id: int
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    phone: PhoneNumber
    grade: GradeDB
    employees: list[EmployeeChild]

    class Config:
        from_attributes = True


class EmployeeDB(EmployeeSchema):
    id: int
