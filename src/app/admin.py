from sqladmin import ModelView

from app.database.models import (Comment, Department, Employee, Grade, Idp,
                                 Post, Task, TaskControl, TaskType)


class EmployeeAdmin(ModelView, model=Employee):
    column_list = ["id", "email", "phone"]
    is_async = True
    category = "Employee"


class GradeAdmin(ModelView, model=Grade):
    column_list = ["id", "title"]
    is_async = True
    category = "Employee"


class PostAdmin(ModelView, model=Post):
    column_list = ["id", "title"]
    is_async = True
    category = "Employee"


class DepartmentAdmin(ModelView, model=Department):
    column_list = ["id", "title"]
    is_async = True
    category = "Employee"


class IdpAdmin(ModelView, model=Idp):
    column_list = [
        "id",
        "title",
        "employee",
        "director",
        "status_idp",
        "date_start",
        "date_end",
    ]
    form_excluded_columns = ["date_start"]
    is_async = True
    category = "Idp"


class TaskAdmin(ModelView, model=Task):
    column_list = [
        "id",
        "name",
        "idp",
        "status_progress",
        "status_accept",
        "task_type",
        "task_control",
    ]
    is_async = True
    category = "Task"


class TaskControlAdmin(ModelView, model=TaskControl):
    column_list = ["id", "title"]
    is_async = True
    category = "Task"


class TaskTypeAdmin(ModelView, model=TaskType):
    column_list = ["id", "name"]
    is_async = True
    category = "Task"


class CommentAdmin(ModelView, model=Comment):
    column_list = ["id", "body_comment", "employee"]
    is_async = True
    category = "Task"


def init(admin_backend):
    admin_backend.add_view(EmployeeAdmin)
    admin_backend.add_view(GradeAdmin)
    admin_backend.add_view(PostAdmin)
    admin_backend.add_view(DepartmentAdmin)
    admin_backend.add_view(IdpAdmin)
    admin_backend.add_view(TaskAdmin)
    admin_backend.add_view(TaskTypeAdmin)
    admin_backend.add_view(TaskControlAdmin)
    admin_backend.add_view(CommentAdmin)
