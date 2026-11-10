"""Infraestructura SQLAlchemy. Alembic es responsable de crear las tablas."""

from contextlib import contextmanager
from pathlib import Path
import os
import sqlite3

from sqlalchemy import create_engine, event
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATABASE_URL = os.environ.get(
    "GASTOS_DATABASE_URL", f"sqlite:///{PROJECT_DIR / 'data' / 'gastos.db'}",
)


class Base(DeclarativeBase):
    """Base común de los modelos; importar el módulo no crea ninguna tabla."""


url = make_url(DATABASE_URL)
engine = create_engine(
    url,
    connect_args={"check_same_thread": False, "timeout": 10}
    if url.get_backend_name() == "sqlite" else {},
)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(connection, _record):
    if isinstance(connection, sqlite3.Connection):
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)


def prepare_database_directory() -> None:
    """Preparar solo el directorio, sin crear o modificar el esquema."""
    if url.get_backend_name() == "sqlite" and url.database not in (None, "", ":memory:"):
        Path(url.database).parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_session():
    """Confirmar al terminar y revertir si falla una operación del servicio."""
    prepare_database_directory()
    with SessionFactory() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
