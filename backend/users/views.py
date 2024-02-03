from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiExample, extend_schema
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


# class EmployeeAPIView(generics.ListAPIView):
#     """Аутентифицированный аккаунт."""

#     permission_classes = [
#         permissions.IsAuthenticated,
#     ]
#     http_method_names = ("get",)

#     def get(self, request, *args, **kwargs):
#         serializer = EmployeeForDirectorSerializer(
#             request.user.employees, max_depth=MAX_DEPTH, many=True
#         )
#         return Response(serializer.data, status=status.HTTP_200_OK)


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

    @extend_schema(
        examples=[
            OpenApiExample(
                "Response",
                value={
                    "id": 27,
                    "director": 4,
                    "first_name": "Alex",
                    "last_name": "Alexov",
                    "patronymic": "Alexovich",
                    "post": "IT-recruiter",
                    "status_idp": "cancelled",
                },
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        examples=[
            OpenApiExample(
                "Response",
                value={
                    "id": 22001,
                    "first_name": "John",
                    "last_name": "Johnov",
                    "patronymic": "Johnovich",
                    "email": "john_superlead@alfa.com",
                    "grade": "Senior+",
                    "post": "Java-developer",
                    "department": "IT",
                    "image": "/way/to/hell.jpg",
                    "hard_skills": {
                        "Структуры данных и алгоритмы": 8,
                        "Инфраструктура разработки": 2,
                        "Аналитическое мышление": 4,
                        "Высшая математика": 8,
                        "average": 5.5,
                    },
                    "soft_skills": {
                        "Наставничество": 10,
                        "Работа в коллективе": 10,
                        "Коммуникабельность": 10,
                        "Аналитическое мышление": 4,
                        "Личная эффективность": 7,
                        "average": 8.2,
                    },
                    "is_director": True,
                    "idps": [
                        {
                            "id": 105,
                            "director": "Samov Sam Samovich",
                            "title": "Super IDP",
                            "progress": 72,
                            "status_idp": "in_work",
                            "current_task": {
                                "id": 780,
                                "name": "Simple task",
                                "date_end": "03.09.2024",
                            },
                        }
                    ],
                },
            )
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        examples=[
            OpenApiExample(
                "Response",
                value={
                    "id": 22001,
                    "first_name": "John",
                    "last_name": "Johnov",
                    "patronymic": "Johnovich",
                    "email": "john_superlead@alfa.com",
                    "grade": "Senior+",
                    "post": "Java-developer",
                    "department": "IT",
                    "image": "/way/to/hell.jpg",
                    "hard_skills": {
                        "Структуры данных и алгоритмы": 8,
                        "Инфраструктура разработки": 2,
                        "Аналитическое мышление": 4,
                        "Высшая математика": 8,
                        "average": 5.5,
                    },
                    "soft_skills": {
                        "Наставничество": 10,
                        "Работа в коллективе": 10,
                        "Коммуникабельность": 10,
                        "Аналитическое мышление": 4,
                        "Личная эффективность": 7,
                        "average": 8.2,
                    },
                    "is_director": True,
                    "idps": [
                        {
                            "id": 105,
                            "director": "Samov Sam Samovich",
                            "title": "Super IDP",
                            "progress": 72,
                            "status_idp": "in_work",
                            "current_task": {
                                "id": 780,
                                "name": "Simple task",
                                "date_end": "03.09.2024",
                            },
                        }
                    ],
                },
            )
        ],
    )
    @action(detail=False, methods=("get",))
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Получить список начальников.",
        responses=DirectorForEmployeeSerializer(many=True),
        examples=[
            OpenApiExample(
                "Response", value={"id": 1, "name": "Johnov John Johnovich"}
            )
        ],
    )
    @action(detail=False, methods=("get",))
    def directors(self, request):
        queryset = request.user.get_ancestors()
        serializer = DirectorForEmployeeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Получить список подчинненых.",
        responses=EmployeeForDirectorSerializer(
            max_depth=MAX_DEPTH, many=True
        ),
        examples=[
            OpenApiExample(
                "Response",
                value={
                    "id": 3,
                    "director": 1,
                    "first_name": "Thomas",
                    "last_name": "Thomasov",
                    "patronymic": "Thomasovich",
                    "post": "Branch Director",
                    "status_idp": "in_work",
                    "subordinates": [
                        {
                            "id": 72,
                            "director": 3,
                            "first_name": "Jessica",
                            "last_name": "Jessicova",
                            "patronymic": "Jessicovna",
                            "post": "Project manager",
                            "status_idp": "done",
                            "subordinates": [
                                {
                                    "id": 1027,
                                    "director": 72,
                                    "first_name": "Peter",
                                    "last_name": "Peterov",
                                    "patronymic": "Petrovich",
                                    "post": "Backend-developer",
                                    "status_idp": "not_completed",
                                    "subordinates": [],
                                }
                            ],
                        }
                    ],
                },
            )
        ],
    )
    @action(detail=False, methods=("get",))
    def get_subordinates(self, request):
        queryset = request.user.employees
        serializer = EmployeeForDirectorSerializer(
            queryset,
            max_depth=MAX_DEPTH,
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
