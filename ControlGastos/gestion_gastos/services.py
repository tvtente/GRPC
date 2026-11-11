"""Interfaces de servicios. Implementación pendiente en las próximas fases.

Cada operación de gastos debe filtrar por el usuario autenticado del servidor.
Nunca aceptar su identidad desde un formulario ni devolver hashes de contraseña.
Las funciones pendientes fallan explícitamente: no simulan un guardado exitoso.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import select

from .database import get_session
from .models import Category, Expense
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
    with get_session() as session:
        statement = (
            select(Expense)
            .where(Expense.user_id == user_id)
            .order_by(Expense.date.desc(), Expense.id.desc())
        )

        expenses = session.scalars(statement).all()

        return [
            ExpenseRead.model_validate(expense)
            for expense in expenses
        ]



def get_expense(expense_id: int, *, user_id: int) -> ExpenseRead:
    with get_session() as session:
        statement = select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == user_id,
        )

        expense = session.scalar(statement)

        if expense is None:
            raise ValueError("Gasto no encontrado.")

        return ExpenseRead.model_validate(expense)



def create_expense(data: ExpenseCreate, *, user_id: int) -> ExpenseRead:
    with get_session() as session:
        expense = Expense(
            description=data.description,
            amount=data.amount,
            date=data.date,
            category_id=data.category_id,
            user_id=user_id,
        )

        session.add(expense)
        session.flush()

        return ExpenseRead.model_validate(expense)



def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    *,
    user_id: int,
) -> ExpenseRead:
    with get_session() as session:
        statement = select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == user_id,
        )

        expense = session.scalar(statement)

        if expense is None:
            raise ValueError("Gasto no encontrado.")

        expense.description = data.description
        expense.amount = data.amount
        expense.date = data.date
        expense.category_id = data.category_id

        session.flush()

        return ExpenseRead.model_validate(expense)




def delete_expense(expense_id: int, *, user_id: int) -> None:
    with get_session() as session:
        statement = select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == user_id,
        )

        expense = session.scalar(statement)

        if expense is None:
            raise ValueError("Gasto no encontrado.")

        session.delete(expense)



def expense_summary(*, user_id: int) -> pd.DataFrame:
    """Pendiente: cargar gastos autorizados y agregar métricas con Pandas."""
    raise NotImplementedError("Análisis con Pandas pendiente.")


def import_excel(path: Path, *, user_id: int) -> int:
    """Pendiente: validar filas y guardar gastos en SQLite en una transacción."""
    raise NotImplementedError("Importación Excel pendiente.")


def export_excel(path: Path, *, user_id: int) -> Path:
    """Pendiente: exportar solo gastos autorizados a Excel con OpenPyXL."""
    raise NotImplementedError("Exportación Excel pendiente.")
