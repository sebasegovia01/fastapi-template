import asyncpg
from os import getenv
from dotenv import load_dotenv

load_dotenv()


async def create_db_connection():
    user = getenv("DB_USER")
    password = getenv("DB_PASSWORD")
    host = getenv("DB_HOST")
    port = getenv("DB_PORT")
    database = getenv("DB_NAME")

    try:
        connection = await asyncpg.connect(
            user=user, password=password, host=host, port=port, database=database
        )
        print("Connection successfully.")
        return connection
    except Exception as e:
        print(f"Connection failed: {e}")
        raise


async def close_db_connection(conn):
    await conn.close()
