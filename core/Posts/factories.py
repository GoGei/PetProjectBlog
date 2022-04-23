import factory
from factory import fuzzy, SubFactory
from django.template.defaultfilters import slugify
from .models import Posts
from core.User.factories import UserFactory


class PostsFactory(factory.DjangoModelFactory):
    author = SubFactory(UserFactory)
    title = fuzzy.FuzzyText(length=255)
    heading = fuzzy.FuzzyText(length=255)
    text = fuzzy.FuzzyText(length=1024)
    slug = factory.LazyAttribute(lambda o: slugify(o.title)[:255])

    class Meta:
        model = Posts
