from pydantic import BaseModel


# Своего рода валидация по аннотации
class EmployeeSchema(BaseModel):
    name: str
    position: str
    department: str
    director: str


class EmployeeDB(EmployeeSchema):
    id: int


# Модель для создания
class GradeSchema(BaseModel):
    title: str


# Модель для создания + новые поля
class GradeDB(GradeSchema):
    id: int
