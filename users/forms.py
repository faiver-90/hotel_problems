from __future__ import annotations

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from common.bootstrap_mixin import BootstrapFormMixin

User = get_user_model()


class StaffLoginForm(BootstrapFormMixin, forms.Form):
    username_or_email = forms.CharField(
        label="Email or username",
        max_length=150,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._init_bootstrap()


class StaffRegisterForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
    )
    language = forms.ChoiceField(
        label="Language",
        required=False,
        choices=User.Language.choices,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2", "language")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._init_bootstrap()

        # Более читабельные лейблы
        self.fields["username"].label = "Username"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Repeat Password"
