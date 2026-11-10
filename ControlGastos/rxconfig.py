"""Configuración independiente para la aplicación académica de gastos."""

import reflex as rx


config = rx.Config(
    app_name="gestion_gastos",
    frontend_port=3002,
    backend_port=8002,
    api_url="http://localhost:8002",
    deploy_url="http://localhost:3002",
    plugins=[
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(appearance="light", accent_color="teal"),
        ),
    ],
    disable_plugins=[rx.plugins.SitemapPlugin],
)
