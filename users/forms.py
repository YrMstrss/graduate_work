from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from content.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('phone', 'password1', 'password2')


class UserProfileChangeForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'birthday', 'city', 'phone', 'avatar', 'username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class AuthForm(StyleFormMixin, AuthenticationForm):
    pass
