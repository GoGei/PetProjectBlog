from django.db import models
from core.Utils.Mixins.models import CrmMixin, ActiveQuerySet


class Contacts(CrmMixin):
    description = models.CharField(max_length=50)
    placeholder = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    link = models.URLField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)

    objects = ActiveQuerySet.as_manager()

    class Meta:
        db_table = 'contacts'

    def __str__(self):
        return self.description
