"""Entrada Reflex: registra la maqueta sin conectar los servicios pendientes."""

import reflex as rx
from .ui_preview import dashboard


def index() -> rx.Component:
    return dashboard()


app = rx.App()
app.add_page(index, route="/", title="Gestión de Gastos Personales")
