from django.db import models
from core.Utils.Mixins.models import CrmMixin, ActiveQuerySet


class About(CrmMixin):
    title = models.CharField(max_length=255)
    heading = models.CharField(max_length=255, null=True)
    text = models.TextField()

    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)

    objects = ActiveQuerySet.as_manager()

    class Meta:
        db_table = 'about'

    def __str__(self):
        return self.title
