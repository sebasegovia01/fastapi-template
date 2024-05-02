# conftest.py
import sys
import os
import asyncpg
import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport


# allow to index app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#  mocks for services

@pytest.fixture
def db_mocks(mocker):
    # Mock the actual connection function used by your application
    mock_conn = AsyncMock(spec=asyncpg.Connection, close=AsyncMock())
    mocker.patch('asyncpg.connect', return_value=mock_conn)
    return mock_conn

@pytest.fixture
def app(db_mocks):
    from app.main import app  # Import here to ensure mocks are in place
    return app

# mocks for db

@pytest.fixture(autouse=True)
def setup_env():
    os.environ["DB_USER"] = "test_user"
    os.environ["DB_PASSWORD"] = "test_pass"
    os.environ["DB_HOST"] = "localhost"
    os.environ["DB_PORT"] = "5432"
    os.environ["DB_NAME"] = "test_db"

# mocks for controller

@pytest.fixture(scope="session")
def db_mocks():
    with patch("app.db.db.create_db_connection", new_callable=AsyncMock) as mock_create:
        mock_conn = AsyncMock()
        mock_create.return_value = mock_conn
        yield mock_conn

@pytest.fixture(scope="session")
def app(db_mocks):
    mock_conn = db_mocks

    async def execute(query, *args):
        if "DELETE FROM" in query and args[0] == 1:
            return "DELETE 1"
        elif "DELETE FROM" in query:
            return "DELETE 0"
        return None

    async def fetch(query, *args):
        if "SELECT" in query and "users" in query:
            return [
                {"id": 1, "userId": "123456789", "userPhoneNumber": "+5691234567"},
                {"id": 2, "userId": "987654321", "userPhoneNumber": "+5698765432"}
            ]
        return []

    async def fetchrow(query, *args):
        if "INSERT INTO" in query:
            return {"id": 3, "userId": args[0], "userPhoneNumber": args[1]}
        elif "SELECT" in query and args[0] == 1:
            return {"id": 1, "userId": "123456789", "userPhoneNumber": "+5691234567"}
        elif "UPDATE" in query and args[2] == 1:
            return {"id": 1, "userId": args[0], "userPhoneNumber": args[1]}
        return None

    mock_conn.execute = execute
    mock_conn.fetch = fetch
    mock_conn.fetchrow = fetchrow
    mock_conn.close = AsyncMock()

    from app.main import app as _app
    yield _app

@pytest.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as _client:
        yield _client
