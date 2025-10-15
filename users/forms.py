from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from config.forms import StyleFormMixin


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "email",
            "avatar",
            "country",
            "phone",
            "password1",
            "password2",
        )


class CustomUserUpdateForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ("avatar", "country", "phone")
