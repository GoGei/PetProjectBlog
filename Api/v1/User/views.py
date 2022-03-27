from django_filters import rest_framework
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from core.User.models import User, Patient, Doctor
from Api.v1.User.serializers import UserSerializer, PatientSerializer, DoctorSerializer, \
    UserCreateSerializer, PatientCreateSerializer, DoctorCreateSerializer


class UserRelatedBaseViewSet(viewsets.ModelViewSet):
    serializer_class = None
    serializer_create_class = None
    user_create_serializer = UserCreateSerializer
    queryset = None

    filter_backends = [filters.SearchFilter, rest_framework.DjangoFilterBackend]
    search_fields = ['user__email', 'user__first_name', 'user__last_name']

    def _create_update_user(self, data, instance=None, **kwargs):
        user_create_data = data.copy()
        user_serializer = self.user_create_serializer(instance, data=user_create_data, **kwargs)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        return user

    def _create_update_related_instance(self, data, user, instance=None, **kwargs):
        patient_create_data = data.copy()
        patient_create_data['user'] = user.pk
        patient_serializer = self.serializer_create_class(instance, data=patient_create_data, **kwargs)
        try:
            patient_serializer.is_valid(raise_exception=True)
        except Exception:
            user.delete()
            raise
        patient = patient_serializer.save()
        return patient

    def create(self, request, *args, **kwargs):
        user = self._create_update_user(request.data)
        patient = self._create_update_related_instance(request.data, user)
        serializer = self.serializer_class(patient)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_instance = instance.user

        user = self._create_update_user(request.data, instance=user_instance, partial=partial)
        patient = self._create_update_related_instance(request.data, user, instance=instance, partial=partial)
        serializer = self.serializer_class(patient)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(instance)
        self.perform_destroy(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserFilter(rest_framework.FilterSet):
    class Meta:
        model = User
        fields = ['is_active', 'is_staff', 'is_superuser']


class PatientFilter(rest_framework.FilterSet):
    class Meta:
        model = Patient
        fields = ['user__is_active']


class DoctorFilter(rest_framework.FilterSet):
    class Meta:
        model = Doctor
        fields = ['user__is_active', 'user__is_staff', 'user__is_superuser']


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    filter_backends = [filters.SearchFilter, rest_framework.DjangoFilterBackend]
    filterset_class = UserFilter
    search_fields = ['user__email', 'user__first_name', 'user__last_name']


class PatientViewSet(UserRelatedBaseViewSet):
    serializer_class = PatientSerializer
    serializer_create_class = PatientCreateSerializer
    queryset = Patient.objects.all()

    filter_backends = [filters.SearchFilter, rest_framework.DjangoFilterBackend]
    filterset_class = PatientFilter
    search_fields = ['user__email', 'user__first_name', 'user__last_name']


class DoctorViewSet(UserRelatedBaseViewSet):
    serializer_class = DoctorSerializer
    serializer_create_class = DoctorCreateSerializer
    queryset = Doctor.objects.all()

    filter_backends = [filters.SearchFilter, rest_framework.DjangoFilterBackend]
    filterset_class = DoctorFilter
    search_fields = ['user__email', 'user__first_name', 'user__last_name']

    def _create_update_user(self, data, instance=None, **kwargs):
        user = super()._create_update_user(data, instance=None, **kwargs)
        user.is_staff = True
        user.save()
        return user
