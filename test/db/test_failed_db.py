from unittest.mock import AsyncMock, patch
import asyncpg
import pytest
from app.db.db import create_db_connection


@pytest.mark.asyncio
async def test_create_db_connection_failure():
    with patch('asyncpg.connect', new_callable=AsyncMock) as mock_connect:
        # Configure the mock to raise an exception simulating a connection failure
        mock_connect.side_effect = asyncpg.exceptions.ConnectionDoesNotExistError("Failed to connect to the database")

        # Attempt to establish a database connection and expect it to raise an exception
        with pytest.raises(asyncpg.exceptions.ConnectionDoesNotExistError) as exc_info:
            await create_db_connection()

        # Ensure the exception message is correct
        assert str(exc_info.value) == "Failed to connect to the database"

        # Verify that the asyncpg.connect method was called with the expected parameters
        mock_connect.assert_called_once_with(
            user="test_user",
            password="test_pass",
            host="localhost",
            port="5432",
            database="test_db"
        )