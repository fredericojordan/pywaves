from django.contrib import admin
from django.contrib.admin import ModelAdmin

from messaging.models import Conversation, WebhookPayload, Message


class ConversationAdmin(ModelAdmin):
    list_display = ("id", "surfer", "created")
    readonly_fields = ("surfer",)
    list_filter = ("surfer", "created")
    search_fields = ("surfer__full_name", "surfer__phone_number")


class MessageAdmin(ModelAdmin):
    list_display = ("id", "surfer", "message_type", "direction", "created")
    readonly_fields = (
        "conversation",
        "surfer",
        "twilio_message_id",
        "message_type",
        "direction",
        "content_url",
        "content_text",
    )
    list_filter = ("message_type", "direction", "created")

    fieldsets = (
        (None, {"fields": ("conversation", "surfer")}),
        ("Twilio fields", {"fields": ("twilio_message_id",)}),
        ("Details", {"fields": ("message_type", "direction")}),
        (
            "Content",
            {"classes": ("collapse",), "fields": ("content_url", "content_text")},
        ),
    )


class WebhookPayloadAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "created")
    list_filter = ("created",)
    readonly_fields = ("url", "payload", "headers")
    fieldsets = (
        (None, {"fields": ("url",)}),
        ("Headers", {"classes": ("collapse",), "fields": ("headers",)}),
        ("Payload", {"classes": ("collapse",), "fields": ("payload",)}),
    )


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(WebhookPayload, WebhookPayloadAdmin)
