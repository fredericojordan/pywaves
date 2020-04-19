from rest_framework import serializers
from rest_framework.serializers import Serializer


class WebhookNewMessageSerializer(Serializer):
    To = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    From = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    Body = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    MessageSid = serializers.CharField(
        required=True, allow_null=False, allow_blank=False
    )


class WebhookMessageStatusSerializer(Serializer):
    To = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    From = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    MessageSid = serializers.CharField(
        required=True, allow_null=False, allow_blank=False
    )
    MessageStatus = serializers.CharField(
        required=True, allow_null=False, allow_blank=False
    )
