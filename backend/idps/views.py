from django.http import HttpResponse
from rest_framework import permissions, viewsets

from idps.serializers import IdpSerializer, EmployeeSerializer
from idps.models import Idp


class IdpViewSet(viewsets.ModelViewSet):
    queryset = Idp.objects.all()
    serializer_class = IdpSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ('get', 'post', 'patch', 'delete')
