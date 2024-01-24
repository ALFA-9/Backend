import time

from django.core.mail import send_mail
from django.db.models import Count, OuterRef, Subquery
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from idps.models import Employee, Idp
from idps.serializers import (CreateIdpSerializer, IdpSerializer,
                              NestedEmployeeSerializer)

SEC_BEFORE_NEXT_REQUEST = 86400

employees_last_request = {}


class IdpViewSet(viewsets.ModelViewSet):
    queryset = Idp.objects.all()
    serializer_class = IdpSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ("get", "post", "patch", "delete")

    def perform_create(self, serializer):
        serializer.save(
            director=Employee.objects.get(id=1)
        )  # self.request.user

    def create(self, request, *args, **kwargs):
        emp_id = request.data["employee"]
        user = Employee.objects.get(id=1)  # self.request.user
        emp = user.get_children().filter(id=emp_id)
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

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return CreateIdpSerializer
        return IdpSerializer


# Проверить после добавления авторизации
@api_view(["POST"])
def idp_request(request):
    employee = request.user  # Для теста Employee.objects.get(id=2)
    # Костыль? можно ли что-то другое придумать, также не хочется трогать бд
    last_request = employees_last_request.setdefault(employee.id, 0)
    time_diff = time.time() - last_request
    if time_diff < SEC_BEFORE_NEXT_REQUEST:
        return Response(
            {"error": "Запрос можно отправлять не чаще 1 раза в сутки."},
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )
    data = request.data
    title = data["title"]
    letter = data["letter"]
    active_idps = Idp.objects.all().filter(
        employee_id=employee.id, status_idp="in_work"
    )
    if active_idps.count() == 0:
        sended = send_mail(title, letter, None, [employee.director_id.email])
        if sended:
            globals().get("employees_last_request")[employee.id] = time.time()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": "Сообщение не отправлено."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(
        {"error": "Вы не можете запросить ИПР, пока не завершено текущее."},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
def get_employees_for_director(request):
    # director = request.user
    employee = Employee.objects.get(id=1)

    serializer = NestedEmployeeSerializer(employee)
    return Response(serializer.data)


@api_view(["GET"])
def get_statistic_for_director(request):
    # director = request.user
    latest_idp_subquery = (
        Idp.objects.filter(employee=OuterRef("pk"))
        .order_by("-date_start", "-id")
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
    return Response(result_dict)
