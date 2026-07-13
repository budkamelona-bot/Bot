import asyncio
from pathlib import Path

import asyncpg

from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "sql" / "001_init.sql"
DATABASE_CONNECT_ATTEMPTS = 10
DATABASE_RETRY_DELAY_SECONDS = 3


async def create_pool() -> asyncpg.Pool:
    for attempt in range(1, DATABASE_CONNECT_ATTEMPTS + 1):
        try:
            return await asyncpg.create_pool(
                dsn=settings.database_url,
                min_size=1,
                max_size=10,
                command_timeout=30,
            )
        except (OSError, asyncpg.PostgresError):
            if attempt == DATABASE_CONNECT_ATTEMPTS:
                raise
            logger.warning(
                "Database is not ready, retrying in %s seconds (%s/%s)",
                DATABASE_RETRY_DELAY_SECONDS,
                attempt,
                DATABASE_CONNECT_ATTEMPTS,
            )
            await asyncio.sleep(DATABASE_RETRY_DELAY_SECONDS)

    raise RuntimeError("Database connection attempts exhausted")


async def initialize_database(pool: asyncpg.Pool) -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    await pool.execute(schema)
