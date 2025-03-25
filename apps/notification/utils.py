from onesignal_sdk.client import Client
from django.conf import settings

def send_push_notification(notification, group=None):
    client = Client(
        app_id=settings.ONESIGNAL_APP_ID,
        rest_api_key=settings.ONESIGNAL_REST_KEY,
        user_auth_key=settings.ONESIGNAL_AUTH_KEY,
    )
    try:
        data = {
            "id": notification.content_id,
            "object_type": notification.type,
            "cover_url": notification.cover_url(),
            "description": notification.description_uz,
            "text": notification.text,
        }
        body = {
            "contents": {"uz": notification.title_uz, "ru": notification.title_ru or notification.title_uz},
            "data": data,
        }
        if group:
            user_ids = [str(user.id) for user in group.students.all()]
            body["include_external_user_ids"] = user_ids
        else:
            body["included_segments"] = ["Active Users"]
        client.send_notification(body)
    except Exception as e:
        print(f"Push notification error: {e}")