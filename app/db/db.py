import string
from typing import Coroutine
import asyncpg
from os import getenv
from dotenv import load_dotenv

load_dotenv()

user = getenv("DB_USER")
password = getenv("DB_PASSWORD")
host = getenv("DB_HOST")
port = getenv("DB_PORT")
database = getenv("DB_NAME")

connection = asyncpg.connect(
    user=user, password=password, host=host, port=port, database=database
)

async def check_db_connection():
    return

async def query(query: string):
    row = connection.execute(query)
    return any(**row) if row else None

async def findById(schema_name: string, table: string, data: any):
    row = connection.fetchrow(f"SELECT * FROM {schema_name}.{table} WHERE {data.key}=$1", data.value)
    return any(**row) if row else None

async def insert():
    return


async def update():
    return

async def delete():
    return