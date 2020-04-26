import logging

from django.conf import settings
from twilio.rest import Client

CLIENT = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
LOGGER = logging.getLogger(__name__)


def create_text_message(message, phone_number, from_number="+14155238886"):
    return CLIENT.messages.create(
        from_=f"whatsapp:{from_number}",
        body=f"{message}",
        to=f"whatsapp:{phone_number}",
    )


def create_media_message(url, phone_number, from_number="+14155238886"):
    return CLIENT.messages.create(
        media_url=url, from_=f"whatsapp:{from_number}", to=f"whatsapp:{phone_number}"
    )


def read_message(message_id):
    try:
        return CLIENT.messages.get(message_id).fetch().body
    except Exception as e:
        LOGGER.error(f"Reading twilio msg #{message_id}: {e}")


def message_list(**kwargs):
    return CLIENT.messages.list(**kwargs)


def parse_phone_number(phone_number):
    return phone_number.replace("whatsapp:", "")
