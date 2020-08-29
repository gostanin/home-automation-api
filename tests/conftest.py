import pytest

from home_automation.app_factory import create_app


@pytest.fixture()
def get_test_client():
    return create_app().test_client()
