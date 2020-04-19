from messaging.models import Conversation, Message
from messaging.utils import read_message, parse_phone_number
from users.models import Surfer


def create_message_objects(message_id, phone_number, direction, content):
    surfer, _ = Surfer.objects.get_or_create(phone_number=phone_number)

    conversation, _ = Conversation.objects.get_or_create(surfer=surfer)

    message, _ = Message.objects.get_or_create(
        conversation=conversation, twilio_message_id=message_id
    )

    message.message_type = Message.TYPE_TEXT
    message.content_text = content
    message.direction = direction
    message.save()

    return message


def process_new_message(request_data):
    phone_number = parse_phone_number(request_data["From"])
    message_id = request_data["MessageSid"]
    content = request_data["Body"]

    return create_message_objects(
        message_id, phone_number, Message.DIRECTION_RECEIVED, content
    )


def process_message_status(request_data):
    if not request_data["MessageStatus"] == "sent":
        return

    message_id = request_data["MessageSid"]
    phone_number = parse_phone_number(request_data["To"])
    content = read_message(message_id)

    return create_message_objects(
        message_id, phone_number, Message.DIRECTION_SENT, content
    )
