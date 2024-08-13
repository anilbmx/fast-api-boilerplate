import os
from pathlib import Path
from sqlalchemy.engine.url import URL

PROJECT_DIR = Path(__file__).parent.parent.parent

def sqlalchemy_database_uri() -> URL:
    PG_HOST = os.environ.get("PG_HOST", "localhost")
    PG_DB = os.environ.get("PG_DB", "postgres")
    PG_USER = os.environ.get("PG_USER", "postgres")
    PG_PASSWORD = os.environ.get("PG_PASSWORD", "password")
    PG_PORT = os.environ.get("PG_PORT", 5432)

    return URL.create(
        drivername="postgresql+asyncpg",
        username=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
    )