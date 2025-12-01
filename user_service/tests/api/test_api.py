from unittest.mock import MagicMock

import pytest
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from app.db.models.user import User


@pytest.fixture
def fake_email(faker):
    return faker.email()


@pytest.fixture(autouse=True)
def mock_verify_password(mocker):
    return mocker.patch(
        "user_service.app.user_service.verify_password", return_value=True
    )


@pytest.fixture
def fake_user_signup_request_data(fake_email, faker):
    return {
        "username": faker.pystr(),
        "email": fake_email,
        "password": faker.pystr(),
    }


@pytest.fixture
def fake_user_login_request_data(fake_user_signup_request_data):
    return {
        "email": fake_user_signup_request_data["email"],
        "password": fake_user_signup_request_data["password"],
    }


@pytest.fixture
def fake_user(fake_user_signup_request_data):
    return User(
        email=fake_user_signup_request_data["email"],
        password=fake_user_signup_request_data["password"],
        username=fake_user_signup_request_data["username"],
    )


@pytest.fixture
def mock_user_repo(mocker):
    def wrapper(get_by_email=None, get_by_id=None, create=None, update_user=None):
        mock_repo = MagicMock()
        mock_repo.get_by_email.return_value = get_by_email
        mock_repo.get_by_id.return_value = get_by_id
        mock_repo.create.return_value = create
        mock_repo.update_user.return_value = update_user

        return mocker.patch(
            "user_service.app.config.dependencies.UserRepository",
            return_value=mock_repo,
        )

    return wrapper


def test_signup_ok(client, fake_user, fake_user_signup_request_data, mock_user_repo):
    mock_user_repo(create=fake_user)

    response = client.post("/signup", json=fake_user_signup_request_data)

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["token_type"] == "bearer"
    assert set(response_json) == {"access_token", "token_type"}


def test_signup_return_400_if_user_exists(
    client, fake_user, fake_user_signup_request_data, mock_user_repo
):
    mock_user_repo(create=fake_user, get_by_email=fake_user)

    response = client.post("/signup", json=fake_user_signup_request_data)

    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["detail"] == "Email already registered"


def test_login_ok(client, fake_user, fake_user_login_request_data, mock_user_repo):
    mock_user_repo(get_by_email=fake_user)

    response = client.post("/login", json=fake_user_login_request_data)

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["token_type"] == "bearer"
    assert set(response_json) == {"access_token", "token_type"}


def test_login_return_401_if_user_not_found(
    client, fake_user_login_request_data, mock_user_repo
):
    mock_user_repo()

    response = client.post("/login", json=fake_user_login_request_data)

    response_json = response.json()
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response_json["detail"] == "Incorrect email or password"
