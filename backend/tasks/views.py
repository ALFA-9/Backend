from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from drf_spectacular.utils import (OpenApiExample, OpenApiRequest,
                                   OpenApiResponse, extend_schema)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from alpha_project.constants import URL
from idps.models import Idp
from tasks.models import Comment, Task
from tasks.serializers import (CommentSerializer, CommentTaskSerializer,
                               TaskGetSerializer, TaskSerializer)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ("post", "patch", "delete")

    @extend_schema(
        request=OpenApiRequest(
            request=TaskSerializer,
            examples=[
                OpenApiExample(
                    "Request",
                    value={
                        "name": "New task",
                        "description": "Not so hard but not so easy",
                        "idp": 120,
                        "type": 1,
                        "status_progress": "in_work",
                        "is_completed": True,
                        "control": 2,
                        "date_start": "03.02.2024",
                        "date_end": "03.12.2024",
                    },
                )
            ],
        ),
        responses={
            201: OpenApiResponse(
                response=TaskGetSerializer,
                examples=[
                    OpenApiExample(
                        "Response",
                        value={
                            "name": "New task",
                            "description": "Not so hard but not so easy",
                            "idp": 120,
                            "type": "Project",
                            "status_progress": "in_work",
                            "is_completed": True,
                            "control": "Test",
                            "date_start": "03.02.2024",
                            "date_end": "03.12.2024",
                        },
                    )
                ],
            )
        },
    )
    def create(self, request, *args, **kwargs):
        current_user = request.user
        idp_id = request.data.get("idp")
        idp = get_object_or_404(Idp, id=idp_id)
        if current_user != idp.director:
            return Response(
                {"error": "Вы не являетесь автором данного ИПР."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        html_content = (
            f'<p>У вас новая задача. <a href="{URL}/employee/idp/{idp_id}'
            '/tasks">ИПР с новой задачей</a>'
        )
        send_mail(
            "Сервис ИПР",
            strip_tags(html_content),
            settings.DEFAULT_FROM_EMAIL,
            [idp.employee.email],
            html_message=html_content,
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @extend_schema(
        request=OpenApiRequest(
            request=TaskSerializer,
            examples=[
                OpenApiExample(
                    "Request",
                    value={
                        "name": "New task",
                        "description": "Not so hard but not so easy",
                        "idp": 120,
                        "type": 1,
                        "status_progress": "in_work",
                        "is_completed": True,
                        "control": 2,
                        "date_start": "03.02.2024",
                        "date_end": "03.12.2024",
                    },
                )
            ],
        ),
        responses={
            201: OpenApiResponse(
                response=TaskGetSerializer,
                examples=[
                    OpenApiExample(
                        "Response",
                        value={
                            "name": "New task",
                            "description": "Not so hard but not so easy",
                            "idp": 120,
                            "type": "Project",
                            "status_progress": "in_work",
                            "is_completed": True,
                            "control": "Test",
                            "date_start": "03.02.2024",
                            "date_end": "03.12.2024",
                        },
                    )
                ],
            )
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        current_user = request.user
        task = self.get_object()

        if task.status_progress != "in_work":
            return Response(
                {"error": "С этой задачей уже нельзя взаимодействовать."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # если текущий пользователь исполнитель задачи
        if current_user == task.idp.employee:
            is_completed = request.data.get("is_completed")
            if is_completed:
                data = {"is_completed": True}
                serializer = self.get_serializer(task, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                director = task.idp.director
                director.email_notifications = F("email_notifications") + (
                    f"<p>Сотрудник пометил задачу {task.name} как "
                    f'выполненную. <a href="{URL}/head/staff/{current_user.id}'
                    f'/{task.idp.id}/tasks">ИПР с задачей</a></p>'
                )
                director.save()

                return Response(serializer.data)

        # если текущий пользователь руководитель исполнителя задачи
        elif current_user == task.idp.director:
            status_progress = request.data.get("status_progress")
            if status_progress != "not_completed":
                data = request.data
                data["is_completed"] = False
                serializer = self.get_serializer(task, data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                html_content = (
                    f'<p>У вас изменился статус задачи {task.name}. <a href="{URL}'
                    f'/employee/idp/{task.idp.id}/tasks">ИПР с этой задачей</a>'
                )
                send_mail(
                    "Сервис ИПР",
                    strip_tags(html_content),
                    settings.DEFAULT_FROM_EMAIL,
                    [task.idp.employee.email],
                    html_message=html_content,
                )
                return Response(serializer.data)

        return Response(
            {"error": "У вас нет прав для изменения статуса задачи."},
            status=status.HTTP_403_FORBIDDEN,
        )

    def destroy(self, request, *args, **kwargs):
        current_user = request.user
        instance = self.get_object()
        task_id = self.kwargs.get("pk")
        task = Task.objects.get(id=task_id)
        if current_user != task.idp.director:
            return Response(
                {"error": "Вы не являетесь автором данного ИПР."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    request=OpenApiRequest(
        request=TaskSerializer,
        examples=[
            OpenApiExample(
                "Request",
                value={
                    "body": "Hello, everyone! Where is gym in our office?",
                },
            )
        ],
    ),
    responses={201: CommentTaskSerializer},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comments(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user not in (task.idp.employee.get_ancestors(include_self=True)):
        return Response(
            {"error": "Вы не моежете оставлять комментарии тут."},
            status=status.HTTP_403_FORBIDDEN,
        )
    employee_id = request.user.id
    body = request.data.get("body")
    serializer = CommentSerializer(
        data={
            "employee": employee_id,
            "task": task_id,
            "body": body,
        },
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, task_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, task=task_id)
    if request.user == comment.employee:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {"error": "Вы не являетесь автором данного комментария."},
        status=status.HTTP_403_FORBIDDEN,
    )
