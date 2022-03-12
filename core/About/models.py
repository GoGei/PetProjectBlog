from django.db import models
from core.Utils.Mixins.models import CrmMixin


class About(CrmMixin):
    title = models.CharField(max_length=255)
    heading = models.CharField(max_length=255, null=True)
    text = models.TextField()
    order_number = models.IntegerField(null=True)

    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)

    class Meta:
        db_table = 'about'

    def __str__(self):
        return self.title
