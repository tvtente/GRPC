"""Alembic usa los mismos modelos, URL y claves foráneas que la aplicación."""

from alembic import context

from gestion_gastos.database import Base, engine, prepare_database_directory
from gestion_gastos import models  # noqa: F401: registrar tablas en Base.metadata


target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=engine.url, target_metadata=target_metadata,
        literal_binds=True, dialect_opts={"paramstyle": "named"},
        render_as_batch=engine.dialect.name == "sqlite",
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    prepare_database_directory()
    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            render_as_batch=engine.dialect.name == "sqlite", compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
