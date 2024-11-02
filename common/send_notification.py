import logging

import firebase_admin
from django.conf import settings
from django.utils import timezone
from firebase_admin import messaging, initialize_app, credentials
from .models import Notification

if not firebase_admin._apps:
    firebase_credentials = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_app = initialize_app(firebase_credentials)

logger = logging.getLogger(__name__)


def send_exam_notification(user, exam):
    title = "Imtihon Eslatmasi"  # Yangi xabarni tayinlang
    message = f"{exam.exam_name} imtihoni {exam.start_time} da boshlanadi."  # Yangi xabarni tayinlang

    if hasattr(user, 'notification_token') and user.notification_token:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=message,
            ),
            token=user.notification_token,
        )
        try:
            response = messaging.send(message)
            logger.info(f"Xabar yuborildi: {response}")

            Notification.objects.create(
                user=user,
                title=title,
                body=message,
                timestamp=timezone.now(),
            )
        except messaging.FirebaseError as e:
            if e.code == 'messaging/registration-token-not-registered':
                logger.warning(f"Noto'g'ri yoki muddati o'tgan token: {user.notification_token}")
            else:
                logger.error(f"Xabar yuborishda xatolik: {e}")
        except Exception as e:
            logger.error(f"Xabar yuborishda umumiy xatolik: {e}")
