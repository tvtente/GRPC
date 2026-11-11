"""Estado Reflex: conexión entre la interfaz y los servicios."""

import reflex as rx

from .services import (
    list_categories,
    list_expenses,
    get_expense,
    create_expense,
    update_expense,
    delete_expense,
)

from .schemas import ExpenseCreate


class AppState(rx.State):
    status: str = "Estructura preparada. Login pendiente."
    error: str = ""
    description: str = ""
    amount: str = ""
    date: str = ""

    selected_expense_id: int | None = None
    username: str = ""
    expenses: list[dict[str, str]] = []

    # Categorías disponibles para el formulario.
    categories: list[dict[str, str]] = []
    selected_category_id: str = ""
    category_error: str = ""

    # ID privado del usuario autenticado.
    _user_id: int | None = None

    # LIMPIAR FORMULARIO

    @rx.event
    def clear_expense_form(self):
        self.description = ""
        self.amount = ""
        self.date = ""
        self.selected_category_id = ""
        self.selected_expense_id = None
        self.error = ""

    # ACTUALIZAR CAMPOS

    @rx.event
    def set_description(self, value: str):
        self.description = value

    @rx.event
    def set_amount(self, value: str):
        self.amount = value

    @rx.event
    def set_date(self, value: str):
        self.date = value

    # CREAR O ACTUALIZAR GASTO

    @rx.event
    def create_expense_event(self):
        if self._user_id is None:
            self.error = "Inicia sesión antes de guardar un gasto."
            return

        try:
            if not self.selected_category_id:
                self.error = "Selecciona una categoría."
                return

            data = ExpenseCreate(
                description=self.description,
                amount=self.amount,
                date=self.date,
                category_id=int(self.selected_category_id),
            )

            if self.selected_expense_id is None:
                create_expense(data, user_id=self._user_id)
                self.status = "Gasto guardado correctamente."
            else:
                update_expense(
                    self.selected_expense_id,
                    data,
                    user_id=self._user_id,
                )
                self.status = "Gasto actualizado correctamente."

            self.clear_expense_form()
            self.load_expenses()

        except Exception as exc:
            self.error = str(exc)

    # CARGAR GASTOS

    @rx.event
    def load_expenses(self):
        if self._user_id is None:
            self.expenses = []
            self.error = "Inicia sesión para consultar tus gastos."
            return

        try:
            items = list_expenses(user_id=self._user_id)

            category_names = {
                category["id"]: category["name"]
                for category in self.categories
            }

            self.expenses = [
                {
                    "id": str(item.id),
                    "description": item.description,
                    "amount": str(item.amount),
                    "date": item.date.isoformat(),
                    "category_id": str(item.category_id),
                    "category": category_names.get(
                        str(item.category_id),
                        "Sin categoría",
                    ),
                }
                for item in items
            ]

            self.error = ""

        except Exception:
            self.expenses = []
            self.error = "No se pudieron cargar los gastos."

    # EDITAR GASTO

    @rx.event
    def edit_expense_event(self, expense_id: str):
        expense_id = int(expense_id)

        if self._user_id is None:
            self.error = "Inicia sesión para editar un gasto."
            return

        try:
            expense = get_expense(
                expense_id,
                user_id=self._user_id,
            )

            self.selected_expense_id = expense.id
            self.description = expense.description
            self.amount = str(expense.amount)
            self.date = expense.date.isoformat()

            self.select_category_for_edit(expense.category_id)

            self.error = ""
            self.status = "Editando gasto."

        except Exception as exc:
            self.error = str(exc)

    # ELIMINAR GASTO

    @rx.event
    def delete_expense_event(self, expense_id: str):
        expense_id = int(expense_id)

        if self._user_id is None:
            self.error = "Inicia sesión para eliminar un gasto."
            return

        try:
            delete_expense(
                expense_id,
                user_id=self._user_id,
            )

            self.clear_expense_form()
            self.load_expenses()
            self.status = "Gasto eliminado correctamente."

        except Exception as exc:
            self.error = str(exc)

    # CATEGORÍAS

    @rx.var
    def category_id(self) -> int | None:
        return (
            int(self.selected_category_id)
            if self.selected_category_id
            else None
        )

    @rx.var
    def category_pending(self) -> bool:
        return not self.selected_category_id

    @rx.event
    def load_categories(self):
        try:
            items = list_categories()

        except Exception:
            self.categories = []
            self.selected_category_id = ""
            self.category_error = (
                "No se pudieron cargar las categorías. "
                "Comprueba que la migración está aplicada."
            )
            return

        self.categories = [
            {"id": str(item.id), "name": item.name}
            for item in items
        ]

        self.category_error = (
            ""
            if self.categories
            else "Todavía no hay categorías. Ejecuta: "
                 "python -m gestion_gastos.seed"
        )

        if self.selected_category_id not in {
            category["id"] for category in self.categories
        }:
            self.selected_category_id = ""

    @rx.event
    def set_selected_category(self, value: str):
        if value in {
            category["id"] for category in self.categories
        }:
            self.selected_category_id = value

    @rx.event
    def select_category_for_edit(self, category_id: int):
        value = str(category_id)

        self.selected_category_id = (
            value
            if value in {
                category["id"] for category in self.categories
            }
            else ""
        )

    # COMPROBAR CONEXIÓN UI

    @rx.event
    def show_status(self):
        self.status = "UI → AppState conectado."
