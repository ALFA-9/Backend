import time

from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from idps.models import Idp
from idps.serializers import CreateIdpSerializer, IdpSerializer

SEC_BEFORE_NEXT_REQUEST = 86400

employees_last_request = {}


class IdpViewSet(viewsets.ModelViewSet):
    queryset = Idp.objects.all()
    serializer_class = IdpSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ("get", "post", "patch", "delete")

    # def perform_create(self, serializer):
    #     serializer.save(employee_id=self.request.user.id,
    #                     director_id=self.request.user.director_id)
    # не забыть убрать эти поля в сериализаторе

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
