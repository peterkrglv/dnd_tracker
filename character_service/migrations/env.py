import sys
import os
import importlib
import pkgutil
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.db.db_vitals import Base

from app.db.models import (
    character,
    character_class,
    characteristics_sheet,
    race,
    users_characters,
    weapon,
)


target_metadata = Base.metadata

USER = os.getenv("CHARACTER_POSTGRES_USER")
PASSWORD = os.getenv("CHARACTER_POSTGRES_PASSWORD")
DB = os.getenv("CHARACTER_POSTGRES_DB")
DB_HOST = os.getenv("CHARACTER_POSTGRES_HOST")
DB_PORT = os.getenv("CHARACTER_POSTGRES_PORT")


SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{DB_HOST}:{DB_PORT}/{DB}"
)

def run_migrations_offline() -> None:
    context.configure(
        url=SQLALCHEMY_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
