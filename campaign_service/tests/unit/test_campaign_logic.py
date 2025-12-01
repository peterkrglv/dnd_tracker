import asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from campaign_service.app.campaign_service import CampaignService
from campaign_service.app.db.models.enums import UserStatus
from campaign_service.app.schemas.campaign_schemas import CampaignCreate


@pytest.fixture
def mock_campaign_repo():
    return MagicMock()


@pytest.fixture
def campaign_service(mock_campaign_repo):
    return CampaignService(campaign_repo=mock_campaign_repo)


def test_get_user_campaigns_returns_list(campaign_service, mock_campaign_repo):
    """
    Тест 1: Проверяет, что `get_user_campaigns` успешно возвращает список кампаний.
    """
    # Arrange
    user_id = uuid4()
    expected_campaigns = [{"id": uuid4(), "name": "My Campaign"}]
    mock_campaign_repo.get_campaigns_by_user_id = AsyncMock(
        return_value=expected_campaigns
    )

    # Act
    result = asyncio.run(campaign_service.get_user_campaigns(user_id=user_id))

    # Assert
    mock_campaign_repo.get_campaigns_by_user_id.assert_called_once_with(user_id)
    assert result == expected_campaigns


def test_create_campaign_calls_repo_methods(campaign_service, mock_campaign_repo):
    """
    Тест 2: Проверяет, что `create_campaign` правильно вызывает методы репозитория.
    """
    # Arrange
    user_id = uuid4()
    campaign_data = CampaignCreate(name="New Adventure", description="A great one")

    created_campaign_mock = MagicMock()
    created_campaign_mock.id = uuid4()

    mock_campaign_repo.create_campaign = AsyncMock(return_value=created_campaign_mock)
    mock_campaign_repo.add_user_to_campaign = AsyncMock()

    # Act
    result = asyncio.run(
        campaign_service.create_campaign(user_id=user_id, campaign_data=campaign_data)
    )

    # Assert
    mock_campaign_repo.create_campaign.assert_called_once_with(
        **campaign_data.model_dump()
    )
    mock_campaign_repo.add_user_to_campaign.assert_called_once_with(
        created_campaign_mock.id, user_id, UserStatus.MASTER
    )
    assert result == created_campaign_mock
