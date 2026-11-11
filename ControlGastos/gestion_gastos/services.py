"""Interfaces de servicios. Implementación pendiente en las próximas fases.

Cada operación de gastos debe filtrar por el usuario autenticado del servidor.
Nunca aceptar su identidad desde un formulario ni devolver hashes de contraseña.
Las funciones pendientes fallan explícitamente: no simulan un guardado exitoso.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import select

from .database import get_session
from .models import Category
from .schemas import CategoryRead, ExpenseCreate, ExpenseRead, ExpenseUpdate, UserCreate, UserLogin, UserRead


def register_user(data: UserCreate) -> UserRead:
    """Pendiente: hash de contraseña y alta con control de duplicados."""
    raise NotImplementedError("Registro pendiente de implementación.")


def authenticate_user(data: UserLogin) -> UserRead:
    """Pendiente: verificar hash y devolver solo datos públicos del usuario."""
    raise NotImplementedError("Login pendiente de implementación.")


def list_categories() -> list[CategoryRead]:
    """Categorías en orden de ID, para el selector del formulario."""
    with get_session() as session:
        rows = session.scalars(select(Category).order_by(Category.id))
        return [CategoryRead.model_validate(row) for row in rows]


def list_expenses(*, user_id: int) -> list[ExpenseRead]:
    raise NotImplementedError("Listado por usuario pendiente.")


def get_expense(expense_id: int, *, user_id: int) -> ExpenseRead:
    raise NotImplementedError("Consulta por ID y propietario pendiente.")


def create_expense(data: ExpenseCreate, *, user_id: int) -> ExpenseRead:
    raise NotImplementedError("Creación de gasto pendiente.")


def update_expense(expense_id: int, data: ExpenseUpdate, *, user_id: int) -> ExpenseRead:
    raise NotImplementedError("Edición por ID y propietario pendiente.")


def delete_expense(expense_id: int, *, user_id: int) -> None:
    raise NotImplementedError("Eliminación por ID y propietario pendiente.")


def expense_summary(*, user_id: int) -> pd.DataFrame:
    """Pendiente: cargar gastos autorizados y agregar métricas con Pandas."""
    raise NotImplementedError("Análisis con Pandas pendiente.")


def import_excel(path: Path, *, user_id: int) -> int:
    """Pendiente: validar filas y guardar gastos en SQLite en una transacción."""
    raise NotImplementedError("Importación Excel pendiente.")


def export_excel(path: Path, *, user_id: int) -> Path:
    """Pendiente: exportar solo gastos autorizados a Excel con OpenPyXL."""
    raise NotImplementedError("Exportación Excel pendiente.")
