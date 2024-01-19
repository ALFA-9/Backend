from pydantic import BaseModel


class GradeDB(BaseModel):
    title: str

    class Config:
        from_attributes = True


class EmployeeSchema(BaseModel):
    grade_id: int
    post_id: int
    department_id: int
    director_id: int
    person_id: int
    grade: GradeDB

    class Config:
        from_attributes = True


class EmployeeDB(EmployeeSchema):
    id: int
