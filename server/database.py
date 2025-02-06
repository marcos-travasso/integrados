import json

import asyncpg


class Database:
    def __init__(self, dsn="postgresql://postgres:postgres@localhost:5433/postgres"):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.dsn, min_size=1, max_size=5)
        async with self.pool.acquire() as conn:
            await conn.execute("CREATE TABLE IF NOT EXISTS rebuilds (id TEXT, status TEXT, received_at TEXT, payload JSONB)")

    async def insert_rebuild(self, id: str, status: str, received_at: str, payload: dict):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO rebuilds (id, status, received_at, payload) VALUES ($1, $2, $3, $4)",
                id, status, received_at, json.dumps(payload)
            )

    async def get_rebuild(self, id: str):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT id, status, received_at, payload FROM rebuilds WHERE id = $1", id)
            return row

    async def close(self):
        if self.pool:
            await self.pool.close()
