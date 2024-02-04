from datetime import datetime

from pydantic import BaseModel, Field, validator


def datetime_format(dt: datetime):
    return dt.strftime("%d.%m.%Y")


def datetime_for_comments_format(dt: datetime):
    return dt.strftime("%d.%m.%y %H:%M")


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
    type_id: int = Field(alias="type")
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
    type_id: int = Field(exclude=True)
    control_id: int = Field(exclude=True)
    status_progress: str
    status_accept: str | None
    task_type: Type = Field(alias="type")
    task_control: Control = Field(alias="control")

    class Config:
        populate_by_name = True
        from_attributes = True
        json_encoders = {
            datetime: datetime_format,
            Type: lambda v: v.name,
            Control: lambda v: v.title,
        }


class Employee(BaseModel):
    first_name: str
    last_name: str
    patronymic: str


class Post(BaseModel):
    title: str


class EmployeePost(BaseModel):
    post: Post

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: datetime_for_comments_format,
            Post: lambda v: v.title,
        }


class Comment(BaseModel): ???
    employee: Employee
    employee_post: Employee
    body_comment: str = Field(alias="body")
    pub_date: datetime = Field(None, examples=["23.11.2024 13:48"])

    class Config:
        populate_by_name = True
        from_attributes = True
        json_encoders = {
            datetime: datetime_for_comments_format,
            Employee: lambda v: f"{v.last_name} {v.first_name} {v.patronymic}",
            EmployeePost: lambda v: v.post,
        }


class TaskWithComments(TaskForIdpCreateDB):
    comments: list[Comment] = Field(alias="comment")

    class Config:
        populate_by_name = True
