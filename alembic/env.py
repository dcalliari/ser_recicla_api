import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para importar a aplicação
sys.path.append(str(Path(__file__).parent.parent))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importar os modelos para que o Alembic possa detectá-los
from app.db.base import Base
from app.db import models  # Isso importa todos os modelos
from app.core.config import settings

# Configuração do Alembic
config = context.config

# Definir a URL do banco de dados
config.set_main_option("sqlalchemy.url", settings.database_url)

# Configurar logs se houver um arquivo de configuração
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados dos modelos para autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
