import pytest

from users.models import User


@pytest.fixture
def user(db):
    user = User.objects.create(
        first_name="Greg", last_name="Graffin", email="graffin@ckl.io"
    )

    user.set_password("american_jesus")
    user.save()

    return user
