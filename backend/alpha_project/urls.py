from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response

from users.models import Employee


# Это здесь для проверки работоспособности
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        childs = self.queryset.get(director=self.request.user.employee)
        employees = childs.get_descendants(include_self=True)
        if employees:
            return employees if employees else self.queryset.none()


router = routers.DefaultRouter()
router.register(r'employee', EmployeeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
