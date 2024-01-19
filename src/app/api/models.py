from pydantic import BaseModel


# Модель для создания
class GradeSchema(BaseModel):
    title: str


# Модель для создания + новые поля
class GradeDB(GradeSchema):
    id: int
