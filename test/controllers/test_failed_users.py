from unittest.mock import AsyncMock, patch
import pytest

# failed get user by id - invalid id
@pytest.mark.asyncio
async def test_get_user(client):
    with patch('app.services.users.get_user_by_id', new_callable=AsyncMock) as mock_get_user_none:
        mock_get_user_none.return_value = {'detail': 'User not found'}
        response = await client.get("/api/v1/users/0")
        assert response.status_code == 404
        assert response.json() == mock_get_user_none.return_value

# failed create new user - invalid userPhoneNumber type
@pytest.mark.asyncio
async def test_create_new_user(client):
    new_user_data = {"userId": "newuser123", "userPhoneNumber": 11111111}
    with patch('app.services.users.create_user', new_callable=AsyncMock) as mock_create_failed:
        mock_create_failed.return_value = "Input should be a valid string"
        response = await client.post("/api/v1/users/", json=new_user_data)
        message = response.json()['detail'][0]['msg']
        assert response.status_code == 422
        assert message == mock_create_failed.return_value

# failed update user - invalid id
@pytest.mark.asyncio
async def test_update_existing_user(client):
    user_data = {"userId": "existing123", "userPhoneNumber": "+5698765432"}

    with patch('app.services.users.update_user', new_callable=AsyncMock) as mock_update_none:
        mock_update_none.return_value = {'detail': 'User not found'}
        response = await client.put("/api/v1/users/0", json=user_data)
        assert response.status_code == 404
        assert response.json() == mock_update_none.return_value

# failed delete user - invalid id
@pytest.mark.asyncio
async def test_delete_existing_user(client):
    with patch('app.services.users.delete_user', new_callable=AsyncMock) as mock_delete_fail:
        mock_delete_fail.return_value = {'detail': 'User not found'}
        response = await client.delete("/api/v1/users/0")
        assert response.status_code == 404
        assert response.json() == mock_delete_fail.return_value