from drf_yasg.inspectors import SwaggerAutoSchema

from messaging.api.v1.serializers import (
    WebhookNewMessageSerializer,
    WebhookMessageStatusSerializer,
)


class WebhookAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys):
        return ["Twilio Webhook Endpoints"]


webhook_new_message = {
    "auto_schema": WebhookAutoSchema,
    "operation_summary": "Twilio New Message Webhook",
    "method": "POST",
    "responses": {200: "Empty BODY"},
    "request_body": WebhookNewMessageSerializer,
}

webhook_message_status = {
    "auto_schema": WebhookAutoSchema,
    "operation_summary": "Twilio Message Status Webhook",
    "method": "POST",
    "responses": {200: "Empty BODY"},
    "request_body": WebhookMessageStatusSerializer,
}
