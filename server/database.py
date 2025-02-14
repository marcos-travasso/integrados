import json

import asyncpg
import psycopg2

class Database:
    def __init__(self, dsn="postgresql://postgres:postgres@localhost:5433/postgres"):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.dsn, min_size=1, max_size=5)
        async with self.pool.acquire() as conn:
            await conn.execute("CREATE TABLE IF NOT EXISTS rebuilds (id TEXT, user_id TEXT, status TEXT, received_at TIMESTAMP DEFAULT NOW(), dimensions INTEGER, payload JSONB, file_path TEXT, started_at TIMESTAMP, finished_at TIMESTAMP, iterations INTEGER, PRIMARY KEY (id))")

    async def insert_rebuild(self, id: str, user_id: str, status: str, dimensions: int, payload: dict):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO rebuilds (id, user_id, status, dimensions, payload) VALUES ($1, $2, $3, $4, $5)",
                id, user_id, status, dimensions, json.dumps(payload)
            )

    async def get_rebuild(self, id: str):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT id, status, received_at, dimensions, file_path, started_at, finished_at, iterations, payload FROM rebuilds WHERE id = $1", id)
            return row

    def update_rebuild(self, id: str, column: str, value = "NOW()"):
        if value != "NOW()" and isinstance(value, str):
            value = f"'{value}'"
        conn = psycopg2.connect(self.dsn)
        conn.autocommit = True
        with conn.cursor() as cur:
            query = f"UPDATE rebuilds SET {column} = {value} WHERE id = %s"
            cur.execute(query, (id,))

    async def close(self):
        if self.pool:
            await self.pool.close()
