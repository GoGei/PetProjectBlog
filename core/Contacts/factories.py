import factory
from factory import fuzzy, faker
from .models import Contacts


class ContactsFactory(factory.DjangoModelFactory):
    description = fuzzy.FuzzyText(length=50)
    placeholder = fuzzy.FuzzyText(length=50)
    field_type = fuzzy.FuzzyChoice(choices=Contacts.CONTACT_FIELDS)

    phone = factory.LazyAttribute(
        lambda o: faker.Faker('phone') if o.field_type == Contacts.PHONE else None)
    link = factory.LazyAttribute(lambda o: faker.Faker('URI') if o.field_type == Contacts.LINK else None)
    email = factory.LazyAttribute(lambda o: faker.Faker('email') if o.field_type == Contacts.EMAIL else None)

    class Meta:
        model = Contacts
