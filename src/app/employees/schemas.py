from pydantic import BaseModel, EmailStr, Field, computed_field, validator

from app.constants import MAX_RECURSION
from app.idps.schemas import IdpForEmployee, IdpWithCurrentTask


class AuthEmployeeSchema(BaseModel):
    email: EmailStr


class EmployeeSchema(BaseModel):
    id: int
    director_id: int = Field(serialization_alias="director")
    first_name: str
    last_name: str
    patronymic: str
    post: str = Field(examples=["Backend-developer"])

    @validator("post", pre=True, always=True)
    def get_post_title(cls, v, values) -> str:
        return v.title

    class Config:
        from_attributes = True


class EmployeeChild(EmployeeSchema):
    max_recursion: int = Field(MAX_RECURSION, exclude=True)
    employees: list["EmployeeChild"]

    @validator("employees", pre=True)
    def get_employees(cls, value, values):
        if values["max_recursion"] > 1:
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


class EmployeeWithIdps(EmployeeSchema):
    idps: list[IdpForEmployee] | None
    department: str = Field(examples=["IT"])
    grade: str = Field(examples=["Senior plus"])
    idps: list[IdpWithCurrentTask] = Field(validation_alias="idp_emp")

    @validator("department", pre=True, always=True)
    def get_department_title(cls, v, values) -> str:
        return v.title

    @validator("grade", pre=True, always=True)
    def get_grade_title(cls, v, values) -> str:
        return v.title


class DirectorSchema(BaseModel):
    id: int
    first_name: str = Field(exclude=True)
    last_name: str = Field(exclude=True)
    patronymic: str = Field(exclude=True)

    @computed_field
    def name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.patronymic}"
