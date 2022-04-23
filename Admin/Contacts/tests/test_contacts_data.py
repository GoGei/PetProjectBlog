from faker import Faker
from core.Contacts.models import Contacts
from factory import fuzzy

faker = Faker()


contacts_data = {
    'description': fuzzy.FuzzyText(length=50).fuzz(),
    'placeholder': fuzzy.FuzzyText(length=50).fuzz(),
    'field_type': fuzzy.FuzzyChoice(choices=Contacts.CONTACT_FIELDS).fuzz(),
}

related_data = {
    Contacts.PHONE: '+38(%s)%s' % (fuzzy.FuzzyText(chars='0123456789', length=2).fuzz(),
                                   fuzzy.FuzzyText(chars='0123456789', length=7).fuzz()),
    Contacts.LINK: faker.url(),
    Contacts.EMAIL: faker.unique.email(),
}

contacts_error_data = {
    'description': fuzzy.FuzzyText(length=60).fuzz(),
    'placeholder': fuzzy.FuzzyText(length=60).fuzz(),
    'field_type': fuzzy.FuzzyChoice(choices=Contacts.CONTACT_FIELDS).fuzz(),
}

contacts_empty_data = {
    'description': None,
}

contacts_filter_form_data = {
    'search': fuzzy.FuzzyText(length=10).fuzz(),
    'is_active': 'true',
    'field_type': fuzzy.FuzzyChoice(choices=Contacts.CONTACT_FIELDS).fuzz(),
}
