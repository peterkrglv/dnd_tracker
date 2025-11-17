# import pytest
# from httpx import AsyncClient,ASGITransport
# from user_service.main import app
#
# @pytest.fixture
# async def client():
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as ac:
#         yield ac
#

import pytest
from fastapi.testclient import TestClient
from user_service.main import app   # где у тебя создан FastAPI()

@pytest.fixture
def client():
    return TestClient(app)


