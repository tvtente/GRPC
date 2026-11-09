"""Aplicación inicial vacía de GRPC."""

import reflex as rx


def index() -> rx.Component:
    return rx.box(min_height="100vh")


app = rx.App()
app.add_page(index, route="/", title="GRPC")
