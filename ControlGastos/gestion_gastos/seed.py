"""Esqueleto de carga inicial. No crea usuarios al importar el módulo."""

DEFAULT_CATEGORIES = (
    "Alimentación", "Transporte", "Vivienda", "Salud", "Educación",
    "Ocio", "Compras", "Servicios", "Otros",
)


def seed_categories() -> None:
    """Pendiente: insertar categorías de forma idempotente tras alembic upgrade."""
    raise NotImplementedError("Carga inicial de categorías pendiente.")


def seed_admin(*, username: str, email: str, password: str) -> None:
    """Pendiente: crear administrador mediante register_user, sin clave fija en Git."""
    raise NotImplementedError("Carga inicial del administrador pendiente.")
