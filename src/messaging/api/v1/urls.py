from django.urls import path

from messaging.api.v1 import views

urlpatterns = [
    path("webhook_new_message", views.webhook_new_message, name="webhook_new_message"),
    path(
        "webhook_message_status",
        views.webhook_message_status,
        name="webhook_message_status",
    ),
]
