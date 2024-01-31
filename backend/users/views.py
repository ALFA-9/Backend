from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import Employee
from .serializers import AuthSerializer, EmployeeSerializer
from .permissions import UserIsDirectorPermission


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


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """Информация о сотрудниках"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [UserIsDirectorPermission]
