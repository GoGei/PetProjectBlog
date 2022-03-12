from django.db import models
from core.Utils.Mixins.models import CrmMixin


class Contacts(CrmMixin):
    CONTACT_FIELDS = ['phone', 'link', 'email']
    PHONE = 'phone'
    LINK = 'link'
    EMAIL = 'email'
    FIELD_TYPE = (
        ('Phone', PHONE),
        ('Link', LINK),
        ('Email', EMAIL),
    )

    description = models.CharField(max_length=50)
    placeholder = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    link = models.URLField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    field_type = models.CharField(max_length=10, choices=FIELD_TYPE, null=True)

    class Meta:
        db_table = 'contacts'

    def __str__(self):
        return self.description

    @property
    def contact_info(self):
        for field in self.CONTACT_FIELDS:
            value = getattr(self, field)
            if value:
                return value
        return None
