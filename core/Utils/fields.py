from django import forms
from django.core.validators import RegexValidator


class PhoneField(forms.CharField):
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                     message=(
                                         "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))

    def __init__(self, *args, **kwargs):
        super(PhoneField, self).__init__(*args, **kwargs)
        self.validators.append(self.phone_validator)
