# conftest.py
import pytest
from unittest.mock import AsyncMock
import asyncpg

# Example test module: test_user_service.py
@pytest.mark.asyncio
async def test_get_user_by_id_found(db_mocks):
    # Setup specific return values for the scenario
    db_mocks.fetchrow.return_value = {"id": 1, "userId": "123456789", "userPhoneNumber": "+5691234567"}
    
    from app.services.users import get_user_by_id
    user = await get_user_by_id(1)
    
    assert user.userId == "123456789"
    assert user.userPhoneNumber == "+5691234567"
    db_mocks.fetchrow.assert_awaited_once_with(
        f"SELECT * FROM sandbox.users WHERE id=$1", 1
    )

# Ensure you use the `db_mocks` fixture to set up any expected database interactions.
