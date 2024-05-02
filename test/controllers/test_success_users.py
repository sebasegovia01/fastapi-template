import pytest
from unittest.mock import AsyncMock, patch


# success get user by id
@pytest.mark.asyncio
async def test_get_user(client):
    with patch(
        "app.services.users.get_user_by_id", new_callable=AsyncMock
    ) as mock_get_user:
        mock_get_user.return_values = {
            "id": 1,
            "userId": "123456789",
            "userPhoneNumber": "+5691234567",
        }
        response = await client.get("/api/v1/users/1")
        assert response.status_code == 200
        assert response.json() == mock_get_user.return_values


# success get user all users
@pytest.mark.asyncio
async def test_get_all_users_filled(client):
    with patch(
        "app.services.users.get_all_users", new_callable=AsyncMock
    ) as mock_get_all:

        mock_get_all.return_value = [
            {"id": 1, "userId": "123456789", "userPhoneNumber": "+5691234567"},
            {"id": 2, "userId": "987654321", "userPhoneNumber": "+5698765432"},
        ]

        response = await client.get("/api/v1/users/")
        assert response.status_code == 200
        json_response = response.json()
        assert json_response == mock_get_all.return_value


# success create new user
@pytest.mark.asyncio
async def test_create_new_user(client):
    new_user_data = {"userId": "newuser123", "userPhoneNumber": "+5698765432"}
    with patch("app.services.users.create_user", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = {"id": 3, **new_user_data}
        response = await client.post("/api/v1/users/", json=new_user_data)
        assert response.status_code == 201
        assert response.json() == {"id": 3, **new_user_data}


# success update user
@pytest.mark.asyncio
async def test_update_existing_user(client):
    user_data = {"userId": "existing123", "userPhoneNumber": "+5698765432"}
    with patch("app.services.users.update_user", new_callable=AsyncMock) as mock_update:
        mock_update.return_value = {"id": 1, **user_data}
        response = await client.put("/api/v1/users/1", json=user_data)
        assert response.status_code == 200
        assert response.json() == {"id": 1, **user_data}


# success update user
@pytest.mark.asyncio
async def test_delete_existing_user(client):
    with patch("app.services.users.delete_user", new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = b'' # empty response
        response = await client.delete("/api/v1/users/1")
        print("response: ", response)
        assert response.status_code == 204
        assert response.content == mock_delete.return_value
