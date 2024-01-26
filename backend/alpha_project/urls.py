from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from djoser.views import UserViewSet as DjoserUserViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from idps.views import (IdpViewSet, get_employees_for_director,
                        get_statistic_for_director, idp_request)
from tasks.views import TaskViewSet

router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"idps", IdpViewSet)
router.register(r"employees", DjoserUserViewSet)

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/request/", idp_request),
    path("api/statistic/", get_statistic_for_director),
    path("api/employees/", get_employees_for_director),
    path(
        "api/tasks/<int:task_id>/comments/",
        TaskViewSet.as_view({"post": "comments"}),
        name="coments",
    ),
    path(
        "api/tasks/<int:task_id>/comments/<int:comment_id>/",
        TaskViewSet.as_view({"delete": "delete_comment"}),
        name="delete_comment",
    ),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="docs",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
