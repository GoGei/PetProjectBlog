import factory
from factory import fuzzy
from .models import TODOModel


class TODOFactory(factory.DjangoModelFactory):
    title = fuzzy.FuzzyText(length=255)
    text = fuzzy.FuzzyText(length=1024)
    priority = fuzzy.FuzzyInteger(low=0)

    class Meta:
        model = TODOModel
