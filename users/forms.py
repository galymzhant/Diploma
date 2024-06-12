from django import forms
from django.core.validators import EmailValidator
from django.db import transaction

from users.models import UserCreateRequest


class CreateUserRequestForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=150, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, validators=[EmailValidator],
                             widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone_number = forms.CharField(max_length=15, required=True,
                                   widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    iin = forms.CharField(required=True, widget=forms.TextInput())
    birth_date = forms.CharField(required=True, widget=forms.DateInput())

    def save(self, commit=True):
        data = self.cleaned_data
        print(data)
        user = UserCreateRequest(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data['phone_number'],
            password=data['password'],
            iin=data['iin'],
            birth_date=data['birth_date']
        )
        if commit:
            with transaction.atomic():
                user.save()
                # If you have additional logic such as sending a verification SMS, it can go here.
                # send_verification_sms(user.phone_number)
        return user
