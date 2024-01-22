from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from idps.views import (IdpViewSet, get_employees_for_director,
                        get_statistic_for_director, idp_request)

router = DefaultRouter()
router.register(r"idps", IdpViewSet)

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/request/", idp_request),
    path("api/statistic/", get_statistic_for_director),
    path("api/employees/", get_employees_for_director),
    # path('api/', include('djoser.urls')),
    path("api/auth/", include("djoser.urls.authtoken")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
