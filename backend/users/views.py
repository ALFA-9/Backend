from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from .constants import MAX_DEPTH
from .models import Employee
from .serializers import (
    AuthSerializer,
    DirectorForEmployeeSerializer,
    DirectorSerializer,
    EmployeeSerializer,
)


class AuthAPIView(generics.GenericAPIView):
    """Авторизация по email."""

    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = AuthSerializer

    @extend_schema(
        description="Авторизация по email.",
        request=AuthSerializer,
        responses={200: {"token": str()}},
    )
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


class EmployeeAPIView(generics.GenericAPIView):
    """Аутентифицированный аккаунт."""

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    http_method_names = ("get",)

    @extend_schema(
        description="Аутентифицированном аккаунте.",
        responses={200: DirectorSerializer(many=True, max_depth=MAX_DEPTH)},
    )
    def get(self, request, *args, **kwargs):
        serializer = DirectorSerializer(request.user, max_depth=MAX_DEPTH)
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

    @action(detail=False, methods=("get",))
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=("get",))
    def directors(self, request):
        queryset = request.user.get_ancestors()
        serializer = DirectorForEmployeeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
