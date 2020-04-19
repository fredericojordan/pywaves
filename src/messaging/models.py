from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Conversation(TimeStampedModel):
    surfer = models.ForeignKey(
        "users.Surfer",
        related_name="conversations",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"{self.surfer.phone_number}"


class Message(TimeStampedModel):
    TYPE_TEXT = "text"
    TYPE_IMAGE = "image"
    TYPE_VIDEO = "video"
    TYPE_AUDIO = "audio"
    MESSAGE_TYPES = (
        (TYPE_TEXT, "Text"),
        (TYPE_IMAGE, "Image"),
        (TYPE_VIDEO, "Video"),
        (TYPE_AUDIO, "Audio"),
    )
    DIRECTION_SENT = "sent"
    DIRECTION_RECEIVED = "received"
    MESSAGE_DIRECTIONS = ((DIRECTION_SENT, "Sent"), (DIRECTION_RECEIVED, "Received"))

    conversation = models.ForeignKey(
        Conversation,
        related_name="messages",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    twilio_message_id = models.CharField(
        _("Twilio's Message ID"), max_length=64, blank=False, null=False
    )
    message_type = models.CharField(
        _("Message Type"), max_length=16, blank=False, null=False, choices=MESSAGE_TYPES
    )
    direction = models.CharField(
        _("Message Direction"),
        max_length=16,
        blank=False,
        null=False,
        choices=MESSAGE_DIRECTIONS,
    )

    content_url = models.URLField(
        _("Message content URL"), max_length=512, blank=True, null=True
    )
    content_text = models.TextField(_("Message content text"), blank=True, null=True)

    def __str__(self):
        return self.twilio_message_id

    @property
    def surfer(self):
        return self.conversation.surfer


class WebhookPayload(TimeStampedModel):
    url = models.URLField(
        _("Webhook Path"),
        null=True,
        blank=True,
        help_text=_("URL path which received the webhook"),
    )
    payload = JSONField(
        _("Webhook Payload"),
        null=True,
        blank=True,
        help_text=_("JSON payload of the received webhook"),
    )
    headers = JSONField(
        _("Webhook Headers"),
        null=True,
        blank=True,
        help_text=_("Request headers of the received webhook"),
    )
