from datetime import datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict


def datetime_format(dt: datetime):
    return dt.strftime("%d.%m.%Y")


def datetime_for_comments_format(dt: datetime):
    return dt.strftime("%d.%m.%y %H:%M")


class Task(BaseModel):
    model_config = ConfigDict(json_encoders = {datetime: datetime_format})

    name: str
    description: str
    idp_id: int
    status_progress: str | None = None
    is_completed: bool | None = None
    date_start: datetime = Field(..., examples=["23.05.2024"])
    date_end: datetime = Field(..., examples=["23.11.2024"])


class TaskDB(Task):
    id: int


class TaskCreate(BaseModel):
    model_config = ConfigDict(json_encoders = {datetime: datetime_format})

    name: str
    description: str
    idp_id: int
    date_start: datetime = Field(..., examples=["23.05.2024"])
    date_end: datetime = Field(..., examples=["23.11.2024"])

    @field_validator("date_end", "date_start", mode="before")
    def parse_date_end(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value


class TaskCreateDB(TaskCreate):
    id: int
    status_progress: str
    is_completed: bool | None = None


class TaskPatch(BaseModel):
    model_config = ConfigDict(json_encoders = {datetime: datetime_format})

    name: str | None = None
    description: str | None = None
    status_progress: str | None = None
    is_completed: bool | None = None
    date_start: datetime | None = Field(None, examples=["23.05.2024"])
    date_end: datetime | None = Field(None, examples=["23.11.2024"])

    @field_validator("date_end", "date_start", mode="before")
    def parse_date_end(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value


class Type(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class Control(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str


class TaskForIdpCreate(BaseModel):
    name: str
    description: str
    type_id: int = Field(alias="type")
    control_id: int = Field(alias="control")
    date_start: datetime | None = Field(None, examples=["23.05.2024"])
    date_end: datetime | None = Field(None, examples=["23.11.2024"])

    @field_validator("date_end", "date_start", mode="before")
    def parse_date_end(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value


class TaskForIdpCreateDB(TaskForIdpCreate):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True, json_encoders={
            datetime: datetime_format,
            Type: lambda v: v.name,
            Control: lambda v: v.title,
        })

    id: int
    type_id: int = Field(exclude=True)
    control_id: int = Field(exclude=True)
    status_progress: str
    is_completed: bool | None = None
    task_type: Type = Field(alias="type", examples=["Project"])
    task_control: Control = Field(alias="control", examples=["Test"])


class Post(BaseModel):
    title: str


class Employee(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    post: Post


class CommentCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    body_comment: str = Field(alias="body")


class Comment(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True, json_encoders={
            datetime: datetime_for_comments_format,
            Employee: lambda v: f"{v.last_name} {v.first_name} {v.patronymic}",
        })

    employee: Employee = Field(examples=["Johnov John Johnovich"])
    employee_post: str = Field(...)
    body_comment: str = Field(alias="body")
    pub_date: datetime = Field(None, examples=["23.11.2024 13:48"])

    @field_validator("employee_post", mode="before")
    def post(cls, v, values) -> str:
        return values["employee"].post.title


class CommentCreateDB(Comment):
    task_id: int


class TaskWithComments(TaskForIdpCreateDB):
    model_config = ConfigDict(populate_by_name=True)

    comment: list[Comment] = Field(alias="comments")


class CurrentTask(BaseModel):
    model_config = ConfigDict(json_encoders={
            datetime: datetime_format,
        })

    id: int
    name: str
    date_end: datetime = Field(examples=["23.11.2024"])
