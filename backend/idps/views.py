import datetime as dt

from django.core.mail import EmailMessage
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from idps.models import Employee, Idp
from idps.permissions import DirectorPermission
from idps.serializers import (CreateIdpScheme, CreateIdpSerializer,
                              IdpWithAllTasksWithComments,
                              IdpWithCurrentTaskSerializer, RequestSerializer)

SEC_BEFORE_NEXT_REQUEST = 86400


class IdpViewSet(viewsets.ModelViewSet):
    queryset = Idp.objects
    serializer_class = IdpWithCurrentTaskSerializer
    permission_classes = [DirectorPermission]
    http_method_names = ("get", "post")

    def perform_create(self, serializer):
        serializer.save(director=self.request.user)

    @extend_schema(request={"application/json": CreateIdpScheme()})
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
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_queryset(self):
        if self.action in ("retrieve"):
            return self.queryset
        return self.queryset.filter(employee=self.request.user)

    def get_serializer_class(self):
        if self.action not in ("list", "retrieve"):
            return CreateIdpSerializer
        elif self.action in ("retrieve"):
            return IdpWithAllTasksWithComments
        return self.serializer_class


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
    responses=RequestSerializer,
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
    last_request = employee.last_request.replace(tzinfo=None)
    if last_request:
        time_diff = (dt.datetime.now() - last_request).total_seconds()
        if time_diff < SEC_BEFORE_NEXT_REQUEST:
            return Response(
                {"error": "Запрос можно отправлять не чаще 1 раза в сутки."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
    serializer = RequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        director = employee.get_ancestors().get(
            id=serializer.data["director_id"]
        )
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
