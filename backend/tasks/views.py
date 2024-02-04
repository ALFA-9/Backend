from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from idps.models import Idp
from tasks.models import Comment, Task
from tasks.serializers import CommentSerializer, TaskSerializer
from users.models import Email


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ("post", "patch", "delete")

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
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

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
                email, _ = Email.objects.get_or_create(
					subject=f"Задача {task.name}",
					body=f"Задача '{task.name}' завершена",
					to=task.idp.director.email
				)
                email.save()
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
                email, _ = Email.objects.get_or_create(
					subject=f"Задача {task.name}",
					body=f"Задача '{task.name}' завершена",
					to=task.idp.director.email
				)
                email.save()
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comments(request, task_id):
    employee_id = request.user.id
    body = request.data.get("body")
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        serializer = CommentSerializer(
            data={
                "employee": employee_id,
                "task": task_id,
                "body": body,
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    queryset = task.comment_task.all()
    serializer = CommentSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, task_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, task=task_id)
    if request.user == comment.employee:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {"error": "Вы не являетесь автором данного комментария."},
        status=status.HTTP_400_BAD_REQUEST,
    )
