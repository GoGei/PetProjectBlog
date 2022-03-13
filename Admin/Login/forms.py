from django import forms
from core.User.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           'autofocus': True}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control'}))

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data['email'].lower()
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Unknown login.')
        return email
