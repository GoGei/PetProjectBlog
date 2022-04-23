import datetime
import factory
from factory import fuzzy
from .models import About


class AboutFactory(factory.DjangoModelFactory):
    title = fuzzy.FuzzyText(length=255)
    heading = fuzzy.FuzzyText(length=255)
    text = fuzzy.FuzzyText(length=1024)
    order_number = fuzzy.FuzzyInteger(low=0, high=100)

    from_date = fuzzy.FuzzyDate(start_date=datetime.datetime.now().date())
    to_date = fuzzy.FuzzyDate(start_date=datetime.datetime.now().date())

    class Meta:
        model = About
