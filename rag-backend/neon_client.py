import asyncpg
from typing import Optional
from config import settings

class NeonClient:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Create a connection pool to Neon Postgres database"""
        try:
            self.pool = await asyncpg.create_pool(
                dsn=settings.NEON_DATABASE_URL,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            print("Connected to Neon Postgres database")
        except Exception as e:
            print(f"Error connecting to Neon database: {e}")
            raise

    async def disconnect(self):
        """Close the connection pool"""
        if self.pool:
            await self.pool.close()

    async def execute_query(self, query: str, *args):
        """Execute a query against the database"""
        if not self.pool:
            raise Exception("Database not connected")

        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def execute_command(self, command: str, *args):
        """Execute a command against the database"""
        if not self.pool:
            raise Exception("Database not connected")

        async with self.pool.acquire() as connection:
            return await connection.execute(command, *args)

# Create a global instance
neon_client = NeonClient()