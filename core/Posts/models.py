from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

from core.User.models import User
from core.Utils.Mixins.models import CrmMixin


class PostClassifier(models.Model):
    OLDER_ORDER = 'older'
    NEWER_ORDER = 'newer'
    DEFAULT_ORDER = NEWER_ORDER
    ORDER_BY_MAP = {
        OLDER_ORDER: 'created_stamp',
        NEWER_ORDER: '-created_stamp',
    }

    TIMEDELTA = timezone.timedelta(days=30)
    RECENTLY_CHANGED = 'recently-changed'
    THIS_MONTH = 'this-month'
    EXTRA_FILTERS = [RECENTLY_CHANGED, THIS_MONTH]

    class Meta:
        abstract = True


class Posts(CrmMixin, PostClassifier):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    heading = models.CharField(max_length=255, null=True)
    text = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.title

    @classmethod
    def is_allowed_to_assign_slug(cls, title, instance=None):
        slug = slugify(title)
        qs = cls.objects.filter(slug=slug)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        return not qs.exists()

    def assign_slug(self):
        slug = slugify(self.title)
        self.slug = slug if len(slug) <= 255 else slug[:255]
        self.save()
        return self
