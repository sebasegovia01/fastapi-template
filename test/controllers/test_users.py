import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

# bd connection mock
@pytest.fixture(scope="session")
def app():
    # Configurar los mocks dentro del ámbito del fixture.
    with patch("app.db.db.create_db_connection", new_callable=AsyncMock) as mock_create:
        mock_conn = AsyncMock()
        mock_create.return_value = mock_conn

        async def execute(query, *args):
            if "DELETE FROM" in query and args[0] == 1:
                return "DELETE 1"
            elif "DELETE FROM" in query:
                return "DELETE 0"
            return None
        
        async def fetch(query):
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

        # Importar la aplicación después de establecer los mocks
        from app.main import app as _app
        yield _app


@pytest.fixture
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as _client:
        yield _client

@pytest.mark.asyncio
async def test_get_user(client):
    response = await client.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "userId": "123456789",
        "userPhoneNumber": "+5691234567",
    }

    response = await client.get("/api/v1/users/0")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_all_users_filled(client):
    with patch('app.services.users.get_all_users', new_callable=AsyncMock) as mock_get_all:
        mock_get_all.return_value = [
            {"id": 1, "userId": "123456789", "userPhoneNumber": "+5691234567"},
            {"id": 2, "userId": "987654321", "userPhoneNumber": "+5698765432"}
        ]
        
        response = await client.get("/api/v1/users/")
        assert response.status_code == 200
        json_response = response.json()
        assert json_response == [
            {"id": 1, "userId": "123456789", "userPhoneNumber": "+5691234567"},
            {"id": 2, "userId": "987654321", "userPhoneNumber": "+5698765432"}
        ]


@pytest.mark.asyncio
async def test_create_new_user(client):
    new_user_data = {"userId": "newuser123", "userPhoneNumber": "+5698765432"}
    with patch('app.services.users.create_user', new_callable=AsyncMock) as mock_create:
        mock_create.return_value = {"id": 3, **new_user_data}
        response = await client.post("/api/v1/users/", json=new_user_data)
        assert response.status_code == 201
        assert response.json() == {"id": 3, **new_user_data}

@pytest.mark.asyncio
async def test_update_existing_user(client):
    user_data = {"userId": "existing123", "userPhoneNumber": "+5698765432"}
    with patch('app.services.users.update_user', new_callable=AsyncMock) as mock_update:
        mock_update.return_value = {"id": 1, **user_data}
        response = await client.put("/api/v1/users/1", json=user_data)
        assert response.status_code == 200
        assert response.json() == {"id": 1, **user_data}

    with patch('app.services.users.update_user', new_callable=AsyncMock) as mock_update_none:
        mock_update_none.return_value = None
        response = await client.put("/api/v1/users/0", json=user_data)
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_existing_user(client):
    with patch('app.services.users.delete_user', new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = "DELETE 1"
        response = await client.delete("/api/v1/users/1")
        assert response.status_code == 204
        assert response.text == ""

    with patch('app.services.users.delete_user', new_callable=AsyncMock) as mock_delete_fail:
        mock_delete_fail.return_value = "DELETE 0"
        response = await client.delete("/api/v1/users/0")
        assert response.status_code == 404

