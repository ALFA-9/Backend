from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Comment, Task
from .serializers import CommentSerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.AllowAny,)

    @action(
        detail=True,
        methods=["get", "post"],
        permission_classes=(permissions.AllowAny,),
    )
    def comments(self, request, pk=None):
        task_id = self.kwargs.get("pk")
        employee = self.request.user
        task = Task.objects.filter(id=task_id)
        if not task.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == "POST":
            serializer = CommentSerializer(
                data={
                    "employee": employee,
                    "task": task_id,
                    "request": request,
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
        permission_classes=(permissions.AllowAny,),
    )
    def delete_comment(self, request, task_id=None, comment_id=None):
        try:
            comment = Comment.objects.get(id=comment_id, task=task_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)