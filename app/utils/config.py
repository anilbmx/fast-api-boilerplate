from pathlib import Path
from sqlalchemy.engine.url import URL

PROJECT_DIR = Path(__file__).parent.parent.parent


PG_HOST = "postgres"
PG_DB = "postgres"
PG_USER: str = "postgres"
PG_PASSWORD = "password"
PG_PORT: int = 5432

def sqlalchemy_database_uri() -> URL:
    return URL.create(
        drivername="postgresql+asyncpg",
        username=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
    )