import os
import asyncio
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from bot.models.base import Base
from bot.models.models import (
    UserWAAMer, Gaz, Wire, Rolls, Robot, Change, Tip, Intestine, Nozzle, Diffuser, Mudguard, Control
)
from bot.models.defect_model import Cleaning, Setting, Defect, MechanicalFault, ProgramError, ModeDeviation, GasProtectionViolation, Event
from bot.models.admin import User
from bot.models.models import Table

# Load environment variables
load_dotenv('.env')

# Alembic Config object
config = context.config
config.set_main_option('sqlalchemy.url', os.environ['DATABASE_URL'])

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with a provided connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'async' mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


# Determine if Alembic is running in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()