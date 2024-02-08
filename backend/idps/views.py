import datetime as dt

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.utils.html import strip_tags
from drf_spectacular.utils import (OpenApiExample, OpenApiRequest,
                                   OpenApiResponse, extend_schema,
                                   inline_serializer)
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from alpha_project.constants import (HTML_NEW_IDP_MESSAGE,
                                     SEC_BEFORE_NEXT_REQUEST, URL)
from idps.models import Employee, Idp
from idps.permissions import CreatorPermission, DirectorPermission
from idps.serializers import (CreateIdpScheme, CreateIdpSerializer,
                              IdpPatchSerializer, IdpWithAllTasksWithComments,
                              IdpWithCurrentTaskSerializer, RequestSerializer)


class IdpViewSet(viewsets.ModelViewSet):
    queryset = Idp.objects
    serializer_class = IdpWithCurrentTaskSerializer
    permission_classes = [DirectorPermission]
    http_method_names = (
        "get",
        "post",
        "patch",
    )

    def perform_create(self, serializer):
        serializer.save(director=self.request.user)
        id = serializer.data["id"]
        title = serializer.data["title"]
        emp_id = serializer.data["employee"]
        emp_email = Employee.objects.get(id=emp_id).email
        html_content = HTML_NEW_IDP_MESSAGE.format(URL=URL, idp_id=id, title=title)
        send_mail(
            "Сервис ИПР",
            strip_tags(html_content),
            settings.DEFAULT_FROM_EMAIL,
            [emp_email],
            html_message=html_content,
        )

    def get_queryset(self):
        if self.action in ("retrieve", "partial_update"):
            return self.queryset
        return self.queryset.filter(employee=self.request.user)

    def get_serializer_class(self):
        if self.action not in ("list", "retrieve", "partial_update"):
            return CreateIdpSerializer
        elif self.action in ("retrieve"):
            return IdpWithAllTasksWithComments
        elif self.action in ("partial_update"):
            return IdpPatchSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == "partial_update":
            return [CreatorPermission()]
        return [permission() for permission in self.permission_classes]

    @extend_schema(
        examples=[
            OpenApiExample(
                name="Response",
                value={
                    "id": 101,
                    "director": "Johnov John Johnovich",
                    "title": "Super IDP",
                    "progress": 68,
                    "status_idp": "in_work",
                    "current_task": {
                        "id": 686,
                        "name": "Simple task",
                        "date_end": "03.06.2024",
                    },
                },
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request={
            "application/json": OpenApiRequest(
                request=CreateIdpScheme,
                examples=[
                    OpenApiExample(
                        "Request",
                        value={
                            "title": "New IDP",
                            "employee": 256,
                            "tasks": [
                                {
                                    "date_start": "03.02.2024",
                                    "name": "First task",
                                    "description": "Read docs",
                                    "date_end": "03.03.2024",
                                    "type": 1,
                                    "control": 2,
                                }
                            ],
                        },
                    )
                ],
            )
        },
        responses={
            201: OpenApiResponse(
                response=CreateIdpSerializer,
                examples=[
                    OpenApiExample(
                        name="Response",
                        value={
                            "title": "Title",
                            "employee": 22001,
                            "director": 1506,
                            "status_idp": "in_work",
                            "tasks": [
                                {
                                    "date_start": "03.02.2024",
                                    "name": "Task",
                                    "description": "Simple task",
                                    "status_progress": "in_work",
                                    "is_completed": False,
                                    "date_end": "03.08.2024",
                                    "type": 1,
                                    "control": 3,
                                }
                            ],
                        },
                    )
                ],
            ),
            404: OpenApiResponse(
                response=Response,
                examples=[
                    OpenApiExample(
                        name="Bad request",
                        value={"error": "Поле 'employee' отсутствует в запросе."},
                    )
                ],
            ),
            403: OpenApiResponse(
                response=Response,
                examples=[
                    OpenApiExample(
                        name="Forbidden",
                        value={
                            "error": "Вы не являетесь начальником для этого сотрудника."
                        },
                    )
                ],
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        emp_id = request.data.get("employee")
        if emp_id is None:
            return Response(
                {"error": "Поле 'employee' отсутствует в запросе."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        emp_id = request.data["employee"]
        user = self.request.user
        emp = user.get_descendants().filter(id=emp_id)
        if emp.exists():
            if emp.get().idp_employee.filter(status_idp="in_work").exists():
                return Response(
                    {"error": "У этого сотрудника уже есть активный ИПР."},
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
        return Response(
            {"error": "Вы не являетесь начальником для этого сотрудника."},
            status=status.HTTP_403_FORBIDDEN,
        )

    @extend_schema(
        examples=[
            OpenApiExample(
                name="Response",
                value={
                    "title": "Title",
                    "employee": 22007,
                    "director": 22001,
                    "status_idp": "in_work",
                    "tasks": [
                        {
                            "id": 708,
                            "name": "Task",
                            "description": "Simple task",
                            "idp": 101,
                            "type": "Project",
                            "status_progress": "in_work",
                            "is_completed": True,
                            "control": "Test",
                            "date_start": "03.02.2024",
                            "date_end": "03.09.2024",
                            "comments": [
                                {
                                    "employee": "Johnov John Johnovich",
                                    "employee_image": "/path/to/success.jpeg",
                                    "employee_post": "IT-recruiter",
                                    "body": "Big text here",
                                    "pub_date": "27.02.2111 20:47",
                                }
                            ],
                        }
                    ],
                },
            )
        ],
        responses={
            201: CreateIdpSerializer,
            403: OpenApiResponse(),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(
    request={
        "multipart/form-data": RequestSerializer(),
        "application/json": inline_serializer(
            "json",
            {
                "director_id": serializers.IntegerField(),
                "title": serializers.CharField(),
                "letter": serializers.CharField(),
            },
        ),
    },
    description="Отправить запрос на ИПР.",
    responses={
        201: RequestSerializer,
        400: OpenApiResponse(
            Response,
            examples=[
                OpenApiExample(
                    name="Bad request",
                    value={"error": "Нельзя запросить ИПР, пока не завершено текущее."},
                )
            ],
        ),
        429: OpenApiResponse(
            Response,
            examples=[
                OpenApiExample(
                    name="Too many requests",
                    value={"error": "Запрос можно отправлять не чаще 1 раза в сутки."},
                )
            ],
        ),
        422: OpenApiResponse(
            Response,
            examples=[
                OpenApiExample(
                    name="Unprocessable entity",
                    value={"error": "Сообщение не отправлено."},
                )
            ],
        ),
    },
    examples=[
        OpenApiExample(
            name="Response",
            value={
                "title": "IDP request",
                "letter": "Please, i need it!",
                "director_id": 106,
                "file": "reasons.doc",
            },
        )
    ],
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def idp_request(request):
    employee = request.user
    if employee.idp_employee.filter(status_idp="in_work").exists():
        return Response(
            {"error": "Нельзя запросить ИПР, пока не завершено текущее."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    last_request = employee.last_request
    if last_request:
        last_request = last_request.replace(tzinfo=None)
        time_diff = (dt.datetime.now() - last_request).total_seconds()
        if time_diff < SEC_BEFORE_NEXT_REQUEST:
            return Response(
                {"error": "Запрос можно отправлять не чаще 1 раза в сутки."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
    serializer = RequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        director = employee.get_ancestors().get(id=serializer.data["director_id"])
    except Employee.DoesNotExist:
        return Response(
            {"error": "Вы не можете отправить запрос данному сотруднику."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    email = EmailMessage(
        subject=serializer.data["title"],
        body=serializer.data["letter"],
        to=[director.email],
    )
    if file := request.FILES.get("file"):
        email.attach(file.name, file.read(), file.content_type)
    sended = email.send()
    if sended:
        employee.last_request = dt.datetime.now()
        employee.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(
        {"error": "Сообщение не отправлено."},
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
