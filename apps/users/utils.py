import jwt

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail


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
