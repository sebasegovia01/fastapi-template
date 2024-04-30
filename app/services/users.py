from typing import Optional
from app.db.db import create_db_connection, close_db_connection
from app.models.users import User

SCHEMA_NAME = "sandbox"


async def get_user_by_id(id: int) -> User | None:
    conn = await create_db_connection()
    row = await conn.fetchrow(f"SELECT * FROM {SCHEMA_NAME}.users WHERE id=$1", id)
    await close_db_connection(conn)
    return User(**row) if row else None


async def get_all_users():
    conn = await create_db_connection()
    rows = await conn.fetch("SELECT * FROM sandbox.users")
    await close_db_connection(conn)
    return [User(**row) for row in rows] if rows else []


async def create_user(user: User) -> User:
    conn = await create_db_connection()
    row = await conn.fetchrow(
        f'INSERT INTO {SCHEMA_NAME}.users ("userId", "userPhoneNumber") VALUES ($1, $2) RETURNING *',
        user.userId,
        user.userPhoneNumber,
    )
    await close_db_connection(conn)
    return User(**row)


async def update_user(id: int, user: User) -> Optional[User]:
    conn = await create_db_connection()
    try:
        row = await conn.fetchrow(
            f'UPDATE {SCHEMA_NAME}.users SET "userId"=$1, "userPhoneNumber"=$2 WHERE id=$3 RETURNING *',
            user.userId,
            user.userPhoneNumber,
            id,
        )
        if row is None:
            return None
        return User(**row)
    finally:
        await close_db_connection(conn)

async def delete_user(id: int):
    conn = await create_db_connection()
    result = await conn.execute(f"DELETE FROM {SCHEMA_NAME}.users WHERE id=$1", id)
    await close_db_connection(conn)
    return result == "DELETE 1"
