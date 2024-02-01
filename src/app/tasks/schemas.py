from datetime import datetime

from pydantic import BaseModel, Field, validator


def datetime_format(dt: datetime):
    return dt.strftime("%d.%m.%Y")


class Task(BaseModel):
    name: str
    description: str
    idp_id: int
    status_progress: str | None = None
    status_accept: str | None = None
    date_start: datetime = Field(..., examples=["23.05.2024"])
    date_end: datetime = Field(..., examples=["23.11.2024"])

    class Config:
        json_encoders = {datetime: datetime_format}


class TaskDB(Task):
    id: int


class TaskCreate(BaseModel):
    name: str
    description: str
    idp_id: int
    date_start: datetime = Field(..., examples=["23.05.2024"])
    date_end: datetime = Field(..., examples=["23.11.2024"])

    @validator("date_end", "date_start", pre=True)
    def parse_date_end(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value

    class Config:
        json_encoders = {datetime: datetime_format}


class TaskCreateDB(TaskCreate):
    id: int
    status_progress: str
    status_accept: str | None = None


class TaskPut(BaseModel):
    name: str | None = None
    description: str | None = None
    status_progress: str | None = None
    status_accept: str | None = None
    date_start: datetime | None = Field(None, examples=["23.05.2024"])
    date_end: datetime | None = Field(None, examples=["23.11.2024"])

    @validator("date_end", "date_start", pre=True)
    def parse_date_end(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value

    class Config:
        json_encoders = {datetime: datetime_format}


class Type(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Control(BaseModel):
    title: str

    class Config:
        from_attributes = True


class TaskForIdpCreate(BaseModel):
    name: str
    description: str
    task_type_id: int = Field(alias="type")
    control_id: int = Field(alias="control")
    date_start: datetime | None = Field(None, examples=["23.05.2024"])
    date_end: datetime | None = Field(None, examples=["23.11.2024"])

    @validator("date_end", "date_start", pre=True)
    def parse_date_end(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value


class TaskForIdpCreateDB(TaskForIdpCreate):
    id: int
    task_type_id: int = Field(exclude=True)
    control_id: int = Field(exclude=True)
    status_progress: str
    status_accept: str | None
    task_type: Type = Field(alias="type")
    control: Control = Field(alias="task_control")

    class Config:
        populate_by_name = True
        from_attributes = True
        json_encoders = {
            datetime: datetime_format,
            Type: lambda v: v.name,
            Control: lambda v: v.title,
        }
