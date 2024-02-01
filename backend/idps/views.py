import time

from django.core.mail import EmailMessage
from django.db.models import Count, OuterRef, Subquery
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from idps.models import Employee, Idp
from idps.permissions import DirectorPermission
from idps.serializers import (CreateIdpSerializer,
                              IdpWithCurrentTaskSerializer, RequestSerializer)

from .permissions import DirectorPermission

SEC_BEFORE_NEXT_REQUEST = 86400

employees_last_request = {}


class IdpViewSet(viewsets.ModelViewSet):
    queryset = Idp.objects
    serializer_class = IdpWithCurrentTaskSerializer
    permission_classes = [DirectorPermission]
    http_method_names = ("get", "post", "patch", "delete")

    def perform_create(self, serializer):
        serializer.save(director=self.request.user)

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
        return self.queryset.filter(employee=self.request.user)

    def get_serializer_class(self):
        if self.action not in ("list"):
            return CreateIdpSerializer
        return self.serializer_class

    @action(
        methods=["get"],
        url_path="employee/(?P<user_id>\d+)",
        detail=False,
    )
    def get_employee_idp(self, request, user_id):
        emp = request.user.get_descendants().filter(id=user_id)
        if not emp.exists():
            return Response(
                {"error": "Вы не являетесь начальником для этого сотрудника."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = Idp.objects.filter(employee__id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(
    parameters=[RequestSerializer],
    description="Отправить запрос на ИПР.",
    responses=RequestSerializer,
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def idp_request(request):
    employee = request.user
    # Костыль? можно ли что-то другое придумать, также не хочется трогать бд
    last_request = employees_last_request.setdefault(employee.id, 0)
    time_diff = time.time() - last_request
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
    active_idps = Idp.objects.filter(
        employee_id=employee.id,
        status_idp="in_work",
    )
    if active_idps.count() == 0:
        email = EmailMessage(
            subject=serializer.data["title"],
            body=serializer.data["letter"],
            to=[director.email],
        )
        if file := request.FILES.get("file"):
            email.attach(file.name, file.read(), file.content_type)
        sended = email.send()
        if sended:
            globals().get("employees_last_request")[employee.id] = time.time()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": "Сообщение не отправлено."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(
        {"error": "Вы не можете запросить ИПР, пока не завершено текущее."},
        status=status.HTTP_400_BAD_REQUEST,
    )


@extend_schema(
    description="Статистика по ИПР всех сотрудников директора",
    responses=inline_serializer(
        "success",
        {
            "in_work": serializers.IntegerField(),
            "canceled": serializers.IntegerField(),
            "done": serializers.IntegerField(),
            "not_completed": serializers.IntegerField(),
            "null": serializers.IntegerField(),
        },
    ),
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_statistic_for_director(request):
    director = request.user
    if director.is_lead_node():
        return Response(
            {"error": "У вас нет подчинненых."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    latest_idp_subquery = (
        Idp.objects.filter(employee=OuterRef("pk"))
        .order_by("-date_start")
        .values("status_idp")[:1]
    )

    # Запрос кол-во различных статусов ИПР, с учетом 1 emp = 1 ИПР(последний)
    result = (
        Employee.objects.get(id=1)
        .get_descendants()
        .annotate(latest_status=Subquery(latest_idp_subquery))
        .values("latest_status")
        .annotate(status_count=Count("id"))
        .values("latest_status", "status_count")
    )

    result_dict = dict(
        (entry["latest_status"], entry["status_count"]) for entry in result
    )
    result_dict.setdefault("in_work", 0)
    result_dict.setdefault("null", 0)
    result_dict.setdefault("not_completed", 0)
    result_dict.setdefault("done", 0)
    result_dict.setdefault("cancelled", 0)

    return Response(result_dict, status=status.HTTP_200_OK)
