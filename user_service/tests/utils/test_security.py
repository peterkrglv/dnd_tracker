import pytest

from app.utils.security import (
    create_access_token,
    decode_token,
    get_password_hash,
    get_user_id_from_token,
    verify_password,
)


@pytest.fixture
def password(faker):
    return faker.pystr()


@pytest.fixture
def user_uuid(faker):
    return faker.uuid4()


@pytest.fixture
def token_data(faker, user_uuid):
    payload = faker.pydict(value_types=[int, str, bool])
    payload["sub"] = user_uuid
    return payload


def test_verify_password(password):
    pass_hash = get_password_hash(password)

    assert verify_password(password, pass_hash)


def test_decode_token(token_data):
    token = create_access_token(token_data)  # arrange

    payload = decode_token(token)  # act

    assert set(payload) == (set(token_data) | {"exp"})


def test_get_user_id_from_token(token_data, user_uuid):
    token = create_access_token(token_data)

    result = get_user_id_from_token(token)

    assert str(result) == user_uuid
