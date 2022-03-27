from django.utils import timezone
from rest_framework import serializers
from Api.v1.User.serializers import DoctorSerializer, PatientSerializer
from core.Appointment.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()

    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient',
            'doctor',
            'appointment_time',
            'date',
            'time',
            'is_paid',
        ]


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient',
            'doctor',
            'date',
            'time',
            'is_paid',
        ]

    def validate(self, data):
        today = timezone.now().date()
        date = data['date']
        time = data['time']

        if today > date:
            raise serializers.ValidationError({'date': 'Date can not be in past'})

        working_hours = Appointment.WORKING_HOURS
        start = working_hours[Appointment.START]
        end = working_hours[Appointment.END]
        if not (start <= time.hour < end):
            raise serializers.ValidationError({'time': 'Time has to be in %s - %s working period' % (start, end)})
        return data
