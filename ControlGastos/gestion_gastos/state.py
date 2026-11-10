"""Esqueleto del estado Reflex: conexión futura entre UI y servicios."""

import reflex as rx


class AppState(rx.State):
    status: str = "Estructura preparada. Login y CRUD pendientes."
    error: str = ""
    username: str = ""
    expenses: list[dict[str, str]] = []
    # Variable privada de backend. No es un campo del formulario ni un setter público.
    # El evento login deberá asignarla solo tras authenticate_user y limpiar al salir.
    _user_id: int | None = None

    @rx.event
    def show_status(self):
        """Evento inocuo para comprobar que la UI se comunica con el estado."""
        self.status = "UI → AppState conectado. Servicios de negocio todavía pendientes."
