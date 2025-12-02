import asyncio
from unittest.mock import MagicMock

from app.handbook_service import HandbookService
from app.schemas.wiki_schemas import WikiItem, WikiItemCreate


def test_create_wiki_item_calls_repository():
    svc = HandbookService()
    mock_repo = MagicMock()

    expected = WikiItem(uuid="abc-123", title="Axe", tag="weapon", content="desc")
    mock_repo.create.return_value = expected

    svc.set_repository(mock_repo)

    item_create = WikiItemCreate(title="Axe", tag="weapon", content="desc")

    result = asyncio.run(svc.create_wiki_item(item_create))

    mock_repo.create.assert_called_once()
    assert isinstance(result, WikiItem)
    assert result.uuid == expected.uuid


def test_get_wiki_list_for_tag_returns_list():
    svc = HandbookService()
    mock_repo = MagicMock()

    expected = [
        WikiItem(uuid="id-1", title="Axe", tag="weapon", content="c1"),
        WikiItem(uuid="id-2", title="Sword", tag="weapon", content="c2"),
    ]
    mock_repo.find_by_tag.return_value = expected

    svc.set_repository(mock_repo)

    result = asyncio.run(svc.get_wiki_list(tag="weapon"))

    mock_repo.find_by_tag.assert_called_once_with("weapon")
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].uuid == "id-1"
