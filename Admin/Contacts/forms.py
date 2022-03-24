import django_filters
from django import forms

from core.Contacts.models import Contacts
from core.Utils.filtersets import BaseFilter
from core.Utils.fields import PhoneField


class ContactsFilter(BaseFilter):
    SEARCH_FIELDS = ['description']

    field_type = django_filters.ChoiceFilter(label='Contact type', empty_label='Not selected',
                                             choices=Contacts.FIELD_TYPE)

    class Meta:
        model = Contacts
        fields = ['field_type'] + BaseFilter.BASE_FILTER_FIELDS


class ContactsForm(forms.ModelForm):
    description = forms.CharField(label='Description', max_length=50, required=True)
    placeholder = forms.CharField(label='Placeholder', max_length=50, required=False)
    phone = PhoneField(label='Phone', max_length=20, required=False)
    link = forms.URLField(label='Link', max_length=255, required=False)
    email = forms.EmailField(label='Email', max_length=255, required=False)

    class Meta:
        model = Contacts
        fields = ['description', 'placeholder', 'phone', 'link', 'email']

    def clean(self):
        cleaned_data = self.cleaned_data
        required_any_field = Contacts.CONTACT_FIELDS
        fields = [cleaned_data.get(field) for field in required_any_field if cleaned_data.get(field)]
        if not fields:
            self.add_error(None, f'It is required fill in any of these fields: {", ".join(required_any_field)}')

        if len(fields) != 1:
            self.add_error(None, f'It is required fill in only one of these fields: {", ".join(required_any_field)}')

        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        instance = super(ContactsForm, self).save(commit=False)

        for key in cleaned_data.keys():
            if key in instance.CONTACT_FIELDS and cleaned_data[key]:
                instance.field_type = key

        if commit:
            instance.save()
        return instance
