import os
import sys
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import create_engine, pool

load_dotenv()

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import the Base from your application's DB setup
from app.db.db_vitals import Base

# Import all models here so that Alembic can see them
from app.db.models import campaign, enums

# Set the metadata for Alembic
target_metadata = Base.metadata

# Get database credentials from environment variables
USER = os.getenv("CAMPAIGN_POSTGRES_USER")
PASSWORD = os.getenv("CAMPAIGN_POSTGRES_PASSWORD")
DB = os.getenv("CAMPAIGN_POSTGRES_DB")
DB_HOST = os.getenv("CAMPAIGN_POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("CAMPAIGN_POSTGRES_PORT", "5432")

# Construct the database URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{DB_HOST}:{DB_PORT}/{DB}"
)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=SQLALCHEMY_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
