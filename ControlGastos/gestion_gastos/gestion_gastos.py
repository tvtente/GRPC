"""Fase 1: página mínima para comprobar que el entorno Reflex funciona."""

import reflex as rx


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.badge("FASE 1 · ENTORNO PREPARADO", color_scheme="teal"),
            rx.heading("Gestión de Gastos Personales", size="7"),
            rx.text("Python · Reflex · Pandas · OpenPyXL", color="gray"),
            rx.callout(
                "El entorno está preparado. El registro de gastos se construirá en las siguientes fases.",
                icon="info",
                color_scheme="teal",
            ),
            align="start",
            spacing="5",
            width="100%",
            max_width="680px",
        ),
        min_height="100vh",
        padding=["24px", "48px"],
    )


app = rx.App()
app.add_page(index, route="/", title="Gestión de Gastos Personales")
