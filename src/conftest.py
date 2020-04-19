import json
import os

import pytest
from rest_framework.authtoken.models import Token

from users.models import User

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def user(db):
    user = User.objects.create(
        first_name="Greg", last_name="Graffin", email="graffin@ckl.io"
    )

    user.set_password("american_jesus")
    user.save()

    return user


@pytest.fixture
def token(db, user):
    token, _ = Token.objects.get_or_create(user=user)
    return token


@pytest.fixture
def webhook_new_message_payload():
    path = "messaging/docs/twilio_webhook_new_message.json"
    return _load_json_content(os.path.join(BASE_DIR, path))


@pytest.fixture
def webhook_message_status_sent_payload():
    path = "messaging/docs/twilio_webhook_message_status_sent.json"
    return _load_json_content(os.path.join(BASE_DIR, path))


@pytest.fixture
def webhook_message_status_delivered_payload():
    path = "messaging/docs/twilio_webhook_message_status_delivered.json"
    return _load_json_content(os.path.join(BASE_DIR, path))


def _load_json_content(path):
    """
    Loads data from a json file
    """
    with open(path, "r") as json_file:
        return json.load(json_file)
