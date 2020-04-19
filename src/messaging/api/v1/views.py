import json
import logging

from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from messaging.api.v1 import docs
from messaging.api.v1.serializers import (
    WebhookNewMessageSerializer,
    WebhookMessageStatusSerializer,
)
from messaging.models import WebhookPayload
from messaging.services import process_new_message, process_message_status

LOGGER = logging.getLogger(__name__)


def log_webhook(request):
    LOGGER.debug(request.headers)
    LOGGER.debug(request.data)

    WebhookPayload.objects.create(
        url=request.get_raw_uri(),
        payload=json.dumps(request.data),
        headers=json.dumps(dict(request.headers)),
    )


@swagger_auto_schema(**docs.webhook_new_message)
@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def webhook_new_message(request):
    log_webhook(request)

    serializer = WebhookNewMessageSerializer(data=request.data)
    if serializer.is_valid():
        process_new_message(request.data)
    else:
        LOGGER.error(f"Error parsing twilio new msg webhook: {serializer.errors}")

    return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(**docs.webhook_message_status)
@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def webhook_message_status(request):
    log_webhook(request)

    serializer = WebhookMessageStatusSerializer(data=request.data)
    if serializer.is_valid():
        process_message_status(request.data)
    else:
        LOGGER.error(f"Error parsing twilio msg status webhook: {serializer.errors}")

    return Response(status=status.HTTP_200_OK)
