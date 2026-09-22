from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password1",
            "password2",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control fc-form-control",
                    "placeholder": "Michael",
                    "autocomplete": "given-name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control fc-form-control",
                    "placeholder": "Ukeje",
                    "autocomplete": "family-name",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "form-control fc-form-control",
                    "placeholder": "michael",
                    "autocomplete": "username",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control fc-form-control",
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control fc-form-control",
                    "placeholder": "+234 800 000 0000",
                    "autocomplete": "tel",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update({
            "class": "form-control fc-form-control",
            "placeholder": "Create a password",
            "autocomplete": "new-password",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control fc-form-control",
            "placeholder": "Confirm your password",
            "autocomplete": "new-password",
        })

    def clean_username(self):
        username = self.cleaned_data["username"].strip().lower()

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "That username is already in use."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or email",
        widget=forms.TextInput(
            attrs={
                "class": "form-control fc-form-control",
                "placeholder": "Username or email",
                "autocomplete": "username",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control fc-form-control",
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        ),
    )

    def clean(self):
        identifier = self.cleaned_data.get("username")

        if identifier:
            identifier = identifier.strip().lower()

            try:
                user = User.objects.get(
                    email__iexact=identifier
                )
                self.cleaned_data["username"] = user.username
            except User.DoesNotExist:
                self.cleaned_data["username"] = identifier

        return super().clean()