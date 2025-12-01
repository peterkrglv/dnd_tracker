from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest
from fastapi import status

from app.config.dependencies import get_campaign_service, get_current_user_id
from app.db.models.campaign import Campaign, UserInCampaign
from app.db.models.enums import UserStatus

TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyODYyYmM5Yi1kMjBiLTQ2MGYtYTEyMC02NDZhN2QzNWRiZDUiLCJleHAiOjE3NjQ3NzU5NTR9.QFPI6tTP4HQCSy81RRc7c01pMqe4ylIyJI7do25cMlU"
AUTH_HEADERS = {"Authorization": f"Bearer {TEST_TOKEN}"}
USER_ID_FROM_TOKEN = UUID("2862bc9b-d20b-460f-a120-646a7d35dbd5")


@pytest.fixture
def mock_campaign_service():
    return MagicMock()


@pytest.fixture(autouse=True)
def override_dependencies(client, mock_campaign_service):
    client.app.dependency_overrides[get_current_user_id] = lambda: USER_ID_FROM_TOKEN
    client.app.dependency_overrides[get_campaign_service] = (
        lambda: mock_campaign_service
    )
    yield
    client.app.dependency_overrides = {}


def test_get_user_campaigns_success(client, mock_campaign_service):
    fake_campaign = Campaign(
        id=uuid4(), name="Test Campaign", description="A cool one."
    )

    fake_association = UserInCampaign(
        user_id=USER_ID_FROM_TOKEN,
        campaign_id=fake_campaign.id,
        status=UserStatus.MASTER,
    )

    fake_campaign.user_associations = [fake_association]

    mock_campaign_service.get_user_campaigns = AsyncMock(return_value=[fake_campaign])

    response = client.get("/campaign/", headers=AUTH_HEADERS)

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["name"] == "Test Campaign"
    assert response_json[0]["is_master"] is True


def test_create_campaign_success(client, mock_campaign_service):
    campaign_name = "The Lost Mines"
    request_data = {"name": campaign_name, "description": "A starter adventure."}

    mock_campaign_object = Campaign(
        id=uuid4(),
        name=campaign_name,
        description="A starter adventure.",
    )

    mock_campaign_service.create_campaign = AsyncMock(return_value=mock_campaign_object)

    response = client.post("/campaign/", json=request_data, headers=AUTH_HEADERS)

    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()
    assert response_json["name"] == campaign_name
    assert response_json["id"] == str(mock_campaign_object.id)
    assert response_json["is_master"] is True
