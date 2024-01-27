from pydantic import BaseModel, EmailStr


class AuthEmployeeSchema(BaseModel):
    email: EmailStr


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
    phone: str

    class Config:
        from_attributes = True


class EmployeeChild(BaseModel):
    id: int
    director_id: int
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    phone: str
    employees: list[EmployeeLastChild]

    class Config:
        from_attributes = True


class EmployeeDB(BaseModel):
    id: int
    grade_id: int
    post_id: int
    department_id: int
    director_id: int
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    phone: str
    grade: GradeDB
    employees: list[EmployeeChild]

    class Config:
        from_attributes = True
