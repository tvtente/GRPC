"""Esqueleto del estado Reflex: conexión futura entre UI y servicios."""

import reflex as rx

from .services import list_categories


class AppState(rx.State):
    status: str = "Estructura preparada. Login y CRUD pendientes."
    error: str = ""
    username: str = ""
    expenses: list[dict[str, str]] = []
    # Categorías: cada elemento es {"id": "3", "name": "Transporte"} (rx.select usa texto).
    categories: list[dict[str, str]] = []
    selected_category_id: str = ""
    category_error: str = ""
    # Variable privada de backend. No es un campo del formulario ni un setter público.
    # El evento login deberá asignarla solo tras authenticate_user y limpiar al salir.
    _user_id: int | None = None

    @rx.event
    def show_status(self):
        """Evento inocuo para comprobar que la UI se comunica con el estado."""
        self.status = "UI → AppState conectado. Servicios de negocio todavía pendientes."

    @rx.var
    def category_id(self) -> int | None:
        """ID para ExpenseCreate / ExpenseUpdate; None si no hay categoría elegida."""
        return int(self.selected_category_id) if self.selected_category_id else None

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
                "Comprueba que la migración está aplicada (alembic upgrade)."
            )
            return
        self.categories = [{"id": str(item.id), "name": item.name} for item in items]
        self.category_error = "" if self.categories else (
            "Todavía no hay categorías. Ejecuta: python -m gestion_gastos.seed"
        )
        if self.selected_category_id not in {c["id"] for c in self.categories}:
            self.selected_category_id = ""

    @rx.event
    def set_selected_category(self, value: str):
        if value in {c["id"] for c in self.categories}:
            self.selected_category_id = value

    @rx.event
    def select_category_for_edit(self, category_id: int):
        """Precargar la categoría de un gasto al editarlo."""
        value = str(category_id)
        self.selected_category_id = value if value in {c["id"] for c in self.categories} else ""
