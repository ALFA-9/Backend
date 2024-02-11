from pydantic import BaseModel, EmailStr, Field, computed_field, field_validator, ConfigDict

from app.api_v1.idps.schemas import IdpForEmployee, IdpWithCurrentTask
from app.constants import MAX_RECURSION


class AuthEmployeeSchema(BaseModel):
    email: EmailStr


class EmployeeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    director_id: int = Field(serialization_alias="director")
    first_name: str
    last_name: str
    patronymic: str
    post: str = Field(examples=["Backend-developer"])

    @field_validator("post", mode="before")
    def get_post_title(cls, v, values) -> str:
        return v.title


class EmployeeChild(EmployeeSchema):
    model_config = ConfigDict(from_attributes=True)

    max_recursion: int = Field(MAX_RECURSION, exclude=True)
    employees: list["EmployeeChild"]

    @field_validator("employees", mode="before")
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


class EmployeeWithIdps(EmployeeSchema):
    idps: list[IdpForEmployee] | None
    department: str = Field(examples=["IT"])
    grade: str = Field(examples=["Senior plus"])
    idps: list[IdpWithCurrentTask] = Field(validation_alias="idp_emp")

    @field_validator("department", mode="before")
    def get_department_title(cls, v, values) -> str:
        return v.title

    @field_validator("grade", mode="before")
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
