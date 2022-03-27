from django.db import models
from core.Utils.Mixins.models import CrmMixin


class Appointment(CrmMixin):
    FORMAT = '%H:%M %d.%m.%Y'
    patient = models.ForeignKey('User.Patient', on_delete=models.PROTECT)
    doctor = models.ForeignKey('User.Doctor', on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField()
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = 'appointment'
        unique_together = [
            ['patient', 'doctor', 'date', 'time']
        ]
        indexes = [
            models.Index(fields=['patient'], name='appointment_patient_idx'),
            models.Index(fields=['doctor'], name='appointment_doctor_idx'),
            models.Index(fields=['date'], name='appointment_date_idx'),
        ]

    def __str__(self):
        return self.label

    @property
    def appointment_time(self):
        return str(self.date) + '' + str(self.time)

    @property
    def label(self):
        string = f'Appointment:\n{self.patient.label}\nby: {self.doctor.label}\non: {self.appointment_time}'
        return string
