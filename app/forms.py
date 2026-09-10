from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "First name",
            "autocomplete": "given-name",
        })
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Last name",
            "autocomplete": "family-name",
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Email address",
            "autocomplete": "email",
        })
    )

    password1 = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "autocomplete": "new-password",
        })
    )

    password2 = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm password",
            "autocomplete": "new-password",
        })
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("The passwords do not match.")

        return cleaned_data


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter 6-digit code",
            "autocomplete": "one-time-code",
            "inputmode": "numeric",
            "maxlength": "6",
        })
    )

    def clean_otp(self):
        otp = self.cleaned_data["otp"].strip()

        if not otp.isdigit():
            raise ValidationError("OTP must contain numbers only.")

        return otp


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Email address",
            "autocomplete": "email",
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "autocomplete": "current-password",
        })
    )