import pytest
from unittest.mock import AsyncMock, patch
import os
import asyncpg

# Assuming create_db_connection and close_db_connection are in app.db.db module
from app.db.db import create_db_connection, close_db_connection

@pytest.mark.asyncio
async def test_create_db_connection_success():
    with patch('asyncpg.connect', new_callable=AsyncMock) as mock_connect:
        # Configure the mock to simulate successful connection
        mock_connect.return_value = AsyncMock(spec=asyncpg.Connection)
        connection = await create_db_connection()

        # Check that a connection object was indeed returned
        assert connection is not None
        # Verify that the asyncpg.connect method was called with the right parameters
        mock_connect.assert_called_once_with(
            user="test_user",
            password="test_pass",
            host="localhost",
            port="5432",
            database="test_db"
        )

@pytest.mark.asyncio
async def test_close_db_connection():
    # Create an async mock for the connection object
    conn = AsyncMock(spec=asyncpg.Connection)
    # Attempt to close the database connection
    await close_db_connection(conn)
    # Check if the close method was awaited once
    conn.close.assert_awaited_once()