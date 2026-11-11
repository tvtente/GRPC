"""Esqueleto de carga inicial. No crea usuarios al importar el módulo.

Categorías iniciales, tras `alembic upgrade`:  python -m gestion_gastos.seed
"""

from sqlalchemy import select

from .database import get_session
from .models import Category

DEFAULT_CATEGORIES = (
    "Alimentación", "Transporte", "Vivienda", "Salud", "Educación",
    "Ocio", "Compras", "Servicios", "Otros",
)


def seed_categories() -> None:
    """Insertar solo las categorías que faltan; no modifica las existentes."""
    with get_session() as session:
        existing = {name.casefold() for name in session.scalars(select(Category.name))}
        for name in DEFAULT_CATEGORIES:
            if name.casefold() not in existing:
                session.add(Category(name=name))


def seed_admin(*, username: str, email: str, password: str) -> None:
    """Pendiente: crear administrador mediante register_user, sin clave fija en Git."""
    raise NotImplementedError("Carga inicial del administrador pendiente.")


if __name__ == "__main__":
    seed_categories()
    print("Categorías iniciales cargadas.")
