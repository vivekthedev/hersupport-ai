from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class UserRegistration(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserRegistration, self).__init__(*args, **kwargs)

        for fieldname in [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].required = True

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email"]
