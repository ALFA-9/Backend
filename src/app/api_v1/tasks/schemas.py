from datetime import datetime

from pydantic import (BaseModel, ConfigDict, Field, field_serializer,
                      field_validator)


def datetime_format(dt: datetime):
    return dt.strftime("%d.%m.%Y")


def datetime_for_comments_format(dt: datetime):
    return dt.strftime("%d.%m.%y %H:%M")


class Task(BaseModel):
    name: str
    description: str
    idp_id: int
    status_progress: str | None = None
    is_completed: bool | None = None
    date_start: datetime = Field(..., examples=["23.05.2024"])
    date_end: datetime = Field(..., examples=["23.11.2024"])

    @field_serializer("date_start", "date_end")
    def serialize_datetime(self, value):
        return datetime_format(value)


class TaskDB(Task):
    id: int


class TaskCreate(BaseModel):
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

    @field_serializer("date_start", "date_end")
    def serialize_datetime(self, value):
        return datetime_format(value)


class TaskCreateDB(TaskCreate):
    id: int
    status_progress: str
    is_completed: bool | None = None


class TaskPatch(BaseModel):
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

    @field_serializer("date_start", "date_end")
    def serialize_datetime(self, value):
        return datetime_format(value)


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
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

    id: int
    type_id: int = Field(exclude=True)
    control_id: int = Field(exclude=True)
    status_progress: str
    is_completed: bool | None = None
    task_type: Type = Field(alias="type", examples=["Project"])
    task_control: Control = Field(alias="control", examples=["Test"])

    @field_serializer("date_start", "date_end")
    def serialize_datetime(self, value):
        return datetime_format(value)

    @field_serializer("task_type")
    def serialize_type(self, value):
        return value.name

    @field_serializer("task_control")
    def serialize_control(self, value):
        return value.title


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
    model_config = ConfigDict(
        from_attributes=True,
    )

    employee: str = Field(validation_alias="employee", examples=["Johnov John Johnovich"])
    employee_post: str = Field(validation_alias="employee")
    body: str = Field(validation_alias="body_comment")
    pub_date: datetime = Field(None, examples=["23.11.2024 13:48"])

    @field_validator("employee_post", mode="before")
    def post(cls, value):
        return value.post.title

    @field_serializer("pub_date")
    def serialize_datetime(self, value):
        return datetime_for_comments_format(value)

    @field_validator("employee", mode="before")
    @classmethod
    def validate_employee(cls, value) -> str:
        return f"{value.last_name} {value.first_name} {value.patronymic}"


class CommentCreateDB(Comment):
    task_id: int


class TaskWithComments(TaskForIdpCreateDB):
    model_config = ConfigDict(populate_by_name=True)

    comment: list[Comment] = Field(alias="comments")


class CurrentTask(BaseModel):
    id: int
    name: str
    date_end: datetime = Field(examples=["23.11.2024"])

    @field_serializer("date_end")
    def serialize_datetime(self, value):
        return datetime_format(value)
