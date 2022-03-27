from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from Api.v1.Speciality.serializers import SpecialitySerializer
from core.Speciality.models import Speciality
from core.User.models import Doctor


class SpecialityViewSet(viewsets.ModelViewSet):
    serializer_class = SpecialitySerializer
    queryset = Speciality.objects.all().ordered()

    @action(detail=True, methods=['get', 'post'])
    def archive(self, request, pk=None):
        obj = self.get_object()
        qs = Doctor.objects.select_related('speciality').filter(speciality=obj)
        if qs.exists():
            return Response({'archive_not_allowed': 'Speciality is used by doctors!'})

        obj.archive(request.user)
        return Response(status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'])
    def restore(self, request, pk=None):
        obj = self.get_object()
        obj.restore(request.user)
        return Response(status.HTTP_200_OK)
