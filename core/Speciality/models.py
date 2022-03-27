from django.db import models
from core.Utils.Mixins.models import CrmMixin


class Speciality(CrmMixin):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        db_table = 'speciality'

    def __str__(self):
        return self.label

    @property
    def label(self):
        return self.name
