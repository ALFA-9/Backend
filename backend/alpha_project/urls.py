from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from idps.views import IdpViewSet, idp_request
from tasks.views import TaskViewSet, comments
from users.views import AuthAPIView, EmployeeViewSet

router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"idps", IdpViewSet)
router.register(r"employees", EmployeeViewSet, basename="employees")

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/request/", idp_request),
    path("api/tasks/<int:task_id>/comments/", comments, name="comments"),
    path("api/auth/", AuthAPIView.as_view(), name="registration"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
