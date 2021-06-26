__all__ = [
    'PhoneForm',
    'PasswordForm',
    'CheckinForm',
    'CreateFormGroup',
    'MessageForm',
    'InviteForm',
]

from django import forms
from django.forms import ModelForm
from authentication.models.user import User
from services.models.chat import *
from services.models.contacts import *
from services.models.mentioning import *
from services.models.message import *


class PhoneForm(forms.Form):
    '''
    A form for entering a phone number
    '''
    phone = forms.CharField(max_length=100)


class PasswordForm(forms.Form):
    '''
    A form for entering a password.
    '''
    password = forms.CharField(max_length=100)


class CheckinForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
        ]


class CreateFormGroup(forms.Form):
    '''
    Form for assigning a name for a new group.
    '''
    name = forms.CharField(max_length=100)


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = [
            'text_message',
        ]

class InviteForm(forms.Form):
    number = forms.CharField(max_length=40)