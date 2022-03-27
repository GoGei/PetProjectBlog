from rest_framework import routers

from Api.v1.User.views import UserViewSet, PatientViewSet, DoctorViewSet
from Api.v1.Speciality.views import SpecialityViewSet
from Api.v1.Appointment.views import AppointmentViewSet

router = routers.DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    router.register('users', UserViewSet, basename='users'),
    router.register('patients', PatientViewSet, basename='patients'),
    router.register('doctors', DoctorViewSet, basename='doctors'),
    router.register('specialities', SpecialityViewSet, basename='specialities'),
    router.register('appointments', AppointmentViewSet, basename='appointments'),
]
