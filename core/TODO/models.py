from django.db import models
from core.Utils.Mixins.models import CrmMixin


class TODOModel(CrmMixin):
    title = models.CharField(max_length=255)
    text = models.TextField()
    priority = models.IntegerField(null=True)

    class Meta:
        db_table = 'todo_model'

    def __str__(self):
        return self.title
