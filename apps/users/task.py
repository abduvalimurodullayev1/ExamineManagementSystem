import random

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import jwt

from apps.users.models import User
from apps.users.utils import send_mail_to_user
from core.celery import app



@shared_task
def send_verification_email(user_id):
    from apps.users.models import User
    user = User.objects.get(id=user_id)
    verification_url = f"{settings.FRONTEND_URL}/verify/{user.verification_token}"
    send_mail(
        subject=_("Verify Your Account"),
        message=_("Click the link to verify your account: ") + verification_url,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )


def register_user(email, password):
    user = User.objects.create_user(email=email, password=password)
    send_verification_email.delay(user.id)
    return user


@shared_task
def send_forgot_password_email(to_email, verification_code):
    subject = 'Parolni tiklash'
    message = f"Parolni tiklash uchun quyidagi kodni kiriting:\n\n{verification_code}\n\nRahmat!"
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [to_email])


def generate_verification_code():
    return str(random.randint(100000, 999999))


@app.task
def send_mail_to_user(user_id: int, user_email: str) -> None:
    token = jwt.encode(
        {
            'user_id': user_id,
            'expired_time': (timezone.now() + timezone.timedelta(seconds=120)).timestamp()
        },
        settings.SECRET_KEY,
        algorithm='HS256'
    )

    subject = "Welcome to Our Website!"
    message = (f"Thank you for joining our website. You're welcome! \n"
               f"http://127.0.0.1:8000/api/v1/users/VerifyEmail/{token}")
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)