"""Modelo de las capturas frame_00061 y siguientes, adaptado a SQLModel actual."""
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from .prioridad import POR_DEFECTO


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Todo(SQLModel, table=True):
    __tablename__ = 'todos'
    __table_args__ = {'sqlite_autoincrement': True}
    id: int | None = Field(default=None,primary_key=True)
    title: str = Field(max_length=160)
    description: str | None = Field(default=None,max_length=3000)
    completed: bool = Field(default=False)
    progress: int = Field(default=0, ge=0, le=100)
    # Cada instancia obtiene su fecha; datetime.now() como valor fijo se evaluaría al importar.
    created_at: datetime = Field(default_factory=utc_now)
    estimated_hours: float = Field(default=0.0, nullable=False)
    due_date: str | None = Field(default=None, max_length=10)
    # LINDEY (adaptación en gustavo): su columna prioridad pasa al modelo común.
    prioridad: str = Field(default=POR_DEFECTO, max_length=16, nullable=False)
