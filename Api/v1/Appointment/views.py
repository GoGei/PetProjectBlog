from django_filters import rest_framework
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from Api.v1.Appointment.serializers import AppointmentSerializer, AppointmentCreateSerializer
from core.Appointment.models import Appointment


class AppointmentFilter(rest_framework.FilterSet):
    class Meta:
        model = Appointment
        fields = ['is_paid', 'date']


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    serializer_create_class = AppointmentCreateSerializer
    queryset = Appointment.objects.all().ordered()
    filterset_class = AppointmentFilter
    filter_backends = [filters.SearchFilter, rest_framework.DjangoFilterBackend]
    search_fields = ['patient__user__email', 'patient__user__first_name', 'patient__user__last_name',
                     'doctor__user__email', 'doctor__user__first_name', 'doctor__user__last_name']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_create_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.serializer_create_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'])
    def pay(self, request, pk=None):
        obj = self.get_object()
        obj.is_paid = True
        obj.save()
        return Response(status.HTTP_200_OK)
