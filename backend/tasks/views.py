from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Comment, Task
from .serializers import CommentSerializer, TaskSerializer
from idps.models import Idp


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        idp_id = request.data["idp"]
        if not Idp.objects.filter(id=idp_id).exists():
            return Response(
                {"error": "Данного ИПР не существует."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        idp = Idp.objects.get(id=idp_id)
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
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        current_user = request.user
        instance = self.get_object()
        task_id = self.kwargs.get("pk")
        task = Task.objects.get(id=task_id)
        employee = task.idp.employee
        # если текущий пользователь исполнитель задачи
        if current_user == employee:
            field_name = "status_progress"
            default = "in_work"
        # если текущий пользователь руководитель исполнителя задачи
        elif current_user in employee.get_ancestors():
            field_name = "status_accept"
            default = "not_accepted"
        else:
            return Response(
                {"error": "У вас нет прав для изменения статуса задачи."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {field_name: request.data.get(field_name, default)}
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

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

    @action(
        detail=True,
        methods=["get"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def employee_tasks(self, request):
        employee = request.user.id
        if Idp.objects.filter(employee=employee).exists():
            idp = Idp.objects.get(employee=employee)
            queryset = idp.task_idp.all()
            serializer = TaskSerializer(instance=queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Idp для данного сотрудника не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        detail=True,
        methods=["get", "post"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def comments(self, request, pk=None):
        task_id = self.kwargs.get("pk")
        employee = request.user.id
        body = request.data.get("body")
        if not Task.objects.filter(id=task_id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not body:
            return Response(
                {"error": "Комментарий отсутствует."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.method == "POST":
            serializer = CommentSerializer(
                data={
                    "employee": employee,
                    "task": task_id,
                    "request": request,
                    "body": body,
                },
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = Comment.objects.filter(task=task_id)
        serializer = CommentSerializer(
            queryset,
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["delete"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def delete_comment(self, request, task_id=None, comment_id=None):
        try:
            comment = Comment.objects.get(id=comment_id, task=task_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
