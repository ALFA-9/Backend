from pydantic import BaseModel


class GradeDB(BaseModel):
    title: str


class EmployeeSchema(BaseModel):
    grade_id: int
    post_id: int
    departament_id: int
    director_id: int
    person_id: int

    class Config:
        orm_mode = True


class EmployeeDB(EmployeeSchema):
    id: int
