from datetime import datetime

from pydantic import (BaseModel, ConfigDict, Field, field_serializer,
                      field_validator)

from app.database.models import Task


def datetime_format(dt: datetime):
    return dt.strftime("%d.%m.%Y")


def datetime_for_comments_format(dt: datetime):
    return dt.strftime("%d.%m.%y %H:%M")


class TaskPatch(BaseModel):
    name: str | None = Field(None, examples=["Simple task"])
    description: str | None = Field(None, examples=["Describe task here"])
    status_progress: Task.StatusProgress | None = None
    is_completed: bool | None = None
    date_start: datetime | None = Field(None, examples=["23.05.2024"])
    date_end: datetime | None = Field(None, examples=["23.11.2024"])

    @field_validator("date_end", "date_start", mode="before")
    def parse_date_end(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value


class TaskForIdpCreate(BaseModel):
    name: str = Field(examples=["Simple task"])
    description: str = Field(examples=["Describe task here"])
    type_id: int = Field(alias="type", examples=[1])
    control_id: int = Field(alias="control", examples=[3])
    date_start: datetime | None = Field(None, examples=["23.05.2024"])
    date_end: datetime | None = Field(None, examples=["23.11.2024"])

    @field_validator("date_end", "date_start", mode="before")
    def parse_date_end(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value


class TaskForIdpCreateDB(TaskForIdpCreate):
    id: int = Field(examples=[6600001])
    type_id: int = Field(exclude=True)
    control_id: int = Field(exclude=True)
    status_progress: Task.StatusProgress
    is_completed: bool = Field(examples=[False])
    type: str = Field(validation_alias="task_type", examples=["Project"])
    control: str = Field(validation_alias="task_control", examples=["Test"])

    @field_serializer("date_start", "date_end")
    def serialize_datetime(self, value):
        return datetime_format(value)

    @field_validator("type", mode="before")
    def validate_type(cls, value):
        return value.name

    @field_validator("control", mode="before")
    def validate_control(cls, value):
        return value.title


class TaskCreate(TaskForIdpCreate):
    idp_id: int = Field(validation_alias="idp", examples=[55001])


class TaskCreateDB(TaskForIdpCreateDB):
    idp_id: int = Field(serialization_alias="idp", examples=[55001])


class CommentCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    body_comment: str = Field(alias="body", examples=["Where is GYM in our office?"])


class Comment(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    employee: str = Field(
        validation_alias="employee", examples=["Johnov John Johnovich"]
    )
    employee_post: str = Field(
        validation_alias="employee", examples=["Android-developer"]
    )
    body: str = Field(
        validation_alias="body_comment", examples=["Where is GYM in our office?"]
    )
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
    task_id: int = Field(examples=[6600001])


class TaskWithComments(TaskForIdpCreateDB):
    model_config = ConfigDict(populate_by_name=True)

    comment: list[Comment] = Field(alias="comments")


class CurrentTask(BaseModel):
    id: int = Field(examples=[6600001])
    name: str = Field(examples=["Hard task"])
    date_end: datetime = Field(examples=["23.11.2024"])

    @field_serializer("date_end")
    def serialize_datetime(self, value):
        return datetime_format(value)
