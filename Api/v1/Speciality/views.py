from django_filters import rest_framework
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from Api.v1.Speciality.serializers import SpecialitySerializer
from core.Speciality.models import Speciality
from core.User.models import Doctor


class SpecialityFilter(rest_framework.FilterSet):
    is_active = rest_framework.BooleanFilter(method='filter_is_active')

    class Meta:
        model = Speciality
        fields = ['is_active']

    def filter_is_active(self, queryset, name, value):
        if value:
            queryset = queryset.active()
        elif not value:
            queryset = queryset.archived()
        return queryset


class SpecialityViewSet(viewsets.ModelViewSet):
    serializer_class = SpecialitySerializer
    queryset = Speciality.objects.all().ordered()

    filterset_class = SpecialityFilter
    filter_backends = [filters.SearchFilter, rest_framework.DjangoFilterBackend]
    search_fields = ['name']

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
