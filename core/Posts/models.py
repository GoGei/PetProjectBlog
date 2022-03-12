from django.db import models
from core.User.models import User
from core.Utils.Mixins.models import CrmMixin


class Posts(CrmMixin):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    heading = models.CharField(max_length=255, null=True)
    text = models.TextField()

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.title
