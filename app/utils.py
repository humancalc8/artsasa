import secrets

from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone


def generate_otp():
    """
    Generate a secure 6-digit OTP.
    """
    return f"{secrets.randbelow(1_000_000):06d}"


def send_verification_otp(user, verification):
    """
    Generate and send a new OTP to the user's email.
    """

    otp = generate_otp()

    expires_at = timezone.now() + timedelta(minutes=10)

    verification.set_otp(
        otp=otp,
        expires_at=expires_at,
    )

    context = {
        "user": user,
        "otp": otp,
        "expires_at": expires_at,
    }

    subject = "Verify your ARTSASA account"

    text_message = f"""
Hello {user.first_name},

Thank you for registering with ARTSASA.

Your email verification code is:

{otp}

This code will expire in 10 minutes.

If you did not create an ARTSASA account, you can ignore this email.

ARTSASA
Contemporary Art Gallery
Nairobi
"""

    html_message = render_to_string(
        "accounts/emails/otp_email.html",
        context
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    email.attach_alternative(
        html_message,
        "text/html"
    )

    email.send()

    return otp