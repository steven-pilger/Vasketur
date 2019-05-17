import os
from django.conf import settings
import pytest

from vasketur.machinestate.utilities import (
    initiate_session,
    authenticate_session,
    request_cookie,
    extract_cookie,
    request_machine_state,
)


@pytest.fixture(scope="session")
def fixture_init_session():
    session = initiate_session()
    return session


@pytest.fixture(scope="session")
def fixture_auth_session(fixture_init_session):
    session = authenticate_session(fixture_init_session)
    return session


@pytest.fixture(scope="session")
def fixture_cookie_request(fixture_init_session):
    cookie_request = request_cookie(fixture_init_session)
    return cookie_request


@pytest.fixture(scope="session")
def fixture_machine_state(fixture_auth_session, fixture_cookie_request):
    c = extract_cookie(fixture_cookie_request)
    rms = request_machine_state(fixture_auth_session, c)
    return rms


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": os.environ["POSTGRES_ENGINE"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
        "NAME": os.environ["POSTGRES_TEST_NAME"],
        "USER": os.environ["POSTGRES_TEST_USER"],
        # "PASSWORD": os.environ["POSTGRES_TEST_PASSWORD"],
    }
