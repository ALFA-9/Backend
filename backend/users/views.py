from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from users.constants import MAX_DEPTH
from users.models import Employee
from users.serializers import (AuthSerializer, DirectorForEmployeeSerializer,
                               EmployeeForDirectorSerializer,
                               EmployeeSerializer, EmployeeWithIdpStatus)


class AuthAPIView(generics.GenericAPIView):
    """Авторизация по email."""

    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            user = get_object_or_404(Employee, email=email)
            token, is_created = Token.objects.get_or_create(user=user)
            success_value = {
                "token": token.key,
            }
            return Response(success_value, status=status.HTTP_200_OK)
        return Response("Неверный запрос", status=status.HTTP_400_BAD_REQUEST)


class EmployeeAPIView(generics.ListAPIView):
    """Аутентифицированный аккаунт."""

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    http_method_names = ("get",)

    def get(self, request, *args, **kwargs):
        serializer = EmployeeForDirectorSerializer(
            request.user.employees, max_depth=MAX_DEPTH, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """Информация о сотрудниках"""

    serializer_class = EmployeeSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^first_name", "^last_name", "^patronymic")

    def get_queryset(self):
        return self.request.user.get_descendants(include_self=False)

    def get_serializer_class(self):
        if self.action == "list":
            return EmployeeWithIdpStatus
        return self.serializer_class

    @action(detail=False, methods=("get",))
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=("get",))
    def directors(self, request):
        queryset = request.user.get_ancestors()
        serializer = DirectorForEmployeeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
