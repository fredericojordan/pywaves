import json

from django.urls import reverse
from rest_framework import status

from messaging.models import Message, WebhookPayload, Conversation


def test_webhook_new_message(db, client, webhook_new_message_payload, mocker):
    create_message_mock = mocker.patch("messaging.utils.create_text_message")

    response = client.post(
        reverse("messaging:webhook_new_message"),
        webhook_new_message_payload,
        content_type="application/json",
    )

    create_message_mock.assert_called_once()

    assert response.status_code == status.HTTP_200_OK

    webhook = WebhookPayload.objects.first()
    assert webhook is not None
    assert json.loads(webhook.payload) == webhook_new_message_payload

    conversation = Conversation.objects.first()
    assert conversation is not None
    assert conversation.surfer.phone_number == "+5548987654321"

    message = Message.objects.first()
    assert message is not None
    assert message.direction == Message.DIRECTION_RECEIVED
    assert message.message_type == Message.TYPE_TEXT
    assert message.conversation == conversation
    assert (
        message.content_text
        == "This is a public service announcement, this is only a test."
    )


def test_webhook_message_status_delivered(
    db, client, webhook_message_status_delivered_payload
):
    response = client.post(
        reverse("messaging:webhook_message_status"),
        webhook_message_status_delivered_payload,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK

    webhook = WebhookPayload.objects.first()
    assert webhook is not None
    assert json.loads(webhook.payload) == webhook_message_status_delivered_payload

    assert not Conversation.objects.exists()
    assert not Message.objects.exists()


def test_webhook_message_status_sent(
    db, client, webhook_message_status_sent_payload, mocker
):
    read_message_mock = mocker.patch("messaging.services.read_message")
    read_message_mock.return_value = "This is a PSA, this is only a test!"

    response = client.post(
        reverse("messaging:webhook_message_status"),
        webhook_message_status_sent_payload,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK

    webhook = WebhookPayload.objects.first()
    assert webhook is not None
    assert json.loads(webhook.payload) == webhook_message_status_sent_payload

    conversation = Conversation.objects.first()
    assert conversation is not None
    assert conversation.surfer.phone_number == "+5548987654321"

    message = Message.objects.get(
        twilio_message_id=webhook_message_status_sent_payload["MessageSid"]
    )
    assert message is not None
    assert message.direction == Message.DIRECTION_SENT
    assert message.message_type == Message.TYPE_TEXT
    assert message.conversation == conversation
    assert message.content_text == "This is a PSA, this is only a test!"
