import httpx
import pytest

BASE_URL = "http://127.0.0.1:8000/api/v1"  # base path

test_user_id = None

# Successfully Cases


@pytest.mark.asyncio
async def test_create_user_succesfully():
    global test_user_id
    new_user = {"userId": "111111111", "userPhoneNumber": "+5691234567"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/users/", json=new_user)
        test_user_id = response.json()["id"]
        assert response.status_code == 201
        assert response.json()["userId"] == new_user["userId"]


@pytest.mark.asyncio
async def test_get_user_succesfully():
    global test_user_id
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users/{test_user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == test_user_id


@pytest.mark.asyncio
async def test_update_user_succesfully():
    global test_user_id
    updated_user = {"userId": "2222222222", "userPhoneNumber": "+569876543"}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{BASE_URL}/users/{test_user_id}", json=updated_user
        )
        assert response.status_code == 200
        assert response.json()["userId"] == updated_user["userId"]


@pytest.mark.asyncio
async def test_delete_user_succesfully():
    global test_user_id
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/users/{test_user_id}")
        assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_all_users_succesfully():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# Error Cases


@pytest.mark.asyncio
async def test_create_user_missing_fields():
    new_user = {"userId": "111111111"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/users/", json=new_user)
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_invalid_format():
    new_user = {"userId": 111111111, "userPhoneNumber": "+569876543"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/users/", json=new_user)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_user_not_found():
    async with httpx.AsyncClient() as client:
        user_id = 0
        response = await client.get(f"{BASE_URL}/users/{user_id}")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_user_invalid_format():
    user_id = "string"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users/{user_id}")
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_user_invalid_format_id():
    user_id = "string"
    updated_user = {"userId": "2222222222", "userPhoneNumber": "+569876543"}
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{BASE_URL}/users/{user_id}", json=updated_user)
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_user_invalid_format_body():
    user_id = "string"
    updated_user = {"userId": "2222222222", "userPhoneNumber": 123456789}
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{BASE_URL}/users/{user_id}", json=updated_user)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_user_id_not_found():
    user_id = 0
    updated_user = {"userId": "2222222222", "userPhoneNumber": "+569876543"}
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{BASE_URL}/users/{user_id}", json=updated_user)
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_user_not_found():
    user_id = 0
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/users/{user_id}")
        assert response.status_code == 404