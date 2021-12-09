import uuid

import pytest


@pytest.fixture(name="random_uuid", scope="session")
def get_uuid():
    def generate_uuid():
        return uuid.uuid4()

    return generate_uuid
