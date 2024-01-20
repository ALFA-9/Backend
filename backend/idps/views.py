from rest_framework import permissions, viewsets

from idps.models import Idp
from idps.serializers import CreateIdpSerializer, IdpSerializer


class IdpViewSet(viewsets.ModelViewSet):
    queryset = Idp.objects.all()
    serializer_class = IdpSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ("get", "post", "patch", "delete")

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return CreateIdpSerializer
        return IdpSerializer
