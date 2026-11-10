"""Maqueta visual: datos ficticios y controles sin acceso a la base de datos.

Este módulo se ocupa solo de presentación. Los avisos identifican los archivos
que conectarán cada sección en las próximas fases.
"""

import reflex as rx
from .work_plan import RESPONSIBILITIES, TEAM_AGREEMENTS, DELIVERY_ORDER


DEMO_EXPENSES = [
    ("01/09/2026", "Vivienda", "Alquiler", "620,00 €", "Transferencia"),
    ("18/09/2026", "Transporte", "Abono y desplazamientos", "98,00 €", "Tarjeta"),
    ("05/10/2026", "Alimentación", "Compra del mes", "380,50 €", "Tarjeta"),
    ("12/10/2026", "Ocio", "Actividades y salidas", "150,00 €", "Efectivo"),
]
CATEGORY_DATA = [
    {"categoria": "Vivienda", "importe": 620},
    {"categoria": "Alimentación", "importe": 380.5},
    {"categoria": "Ocio", "importe": 150},
    {"categoria": "Transporte", "importe": 98},
]
MONTH_DATA = [
    {"mes": "Septiembre", "importe": 718},
    {"mes": "Octubre", "importe": 530.5},
]


def pending(message: str, files: str) -> rx.Component:
    return rx.box(
        rx.hstack(rx.icon("construction", size=15), rx.text(message, size="2"), align="center"),
        rx.text(files, size="1", color="#64748b", margin_top="4px", overflow_wrap="anywhere"),
        padding="12px", background="#f8fafc", border_radius="8px", width="100%",
    )


def panel(title: str, subtitle: str, *children) -> rx.Component:
    return rx.box(
        rx.heading(title, size="4", color="#0f172a"),
        rx.text(subtitle, size="2", color="#64748b", margin_top="4px", margin_bottom="20px"),
        rx.vstack(*children, spacing="4", align="stretch", width="100%"),
        padding=["20px", "28px"], background="white", border="1px solid #e2e8f0",
        border_radius="16px", box_shadow="0 4px 18px #0f172a04", min_width="0",
    )


def kpi(label: str, value: str, detail: str, icon: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text(label, size="2", color="#64748b"), rx.spacer(),
            rx.icon(icon, size=18, color="#0d9488"), width="100%", align="center",
        ),
        rx.heading(value, size="7", margin_top="14px", color="#0f172a"),
        rx.text(detail, size="1", color="#64748b", margin_top="8px"),
        padding="24px", border_radius="14px", border="1px solid #e2e8f0", background="white",
    )


def expense_table() -> rx.Component:
    return rx.box(
        rx.table.root(
            rx.table.header(rx.table.row(*[
                rx.table.column_header_cell(label)
                for label in ["Fecha", "Categoría", "Descripción", "Importe", "Pago", "Acciones"]
            ])),
            rx.table.body(*[
                rx.table.row(
                    rx.table.cell(row[0]),
                    rx.table.cell(rx.badge(row[1], color_scheme="teal", variant="soft")),
                    rx.table.cell(row[2]),
                    rx.table.cell(rx.text(row[3], weight="bold")),
                    rx.table.cell(row[4]),
                    rx.table.cell(rx.hstack(
                        rx.button("Editar", size="1", variant="soft", disabled=True),
                        rx.button("Eliminar", size="1", variant="soft", color_scheme="red", disabled=True),
                    )),
                ) for row in DEMO_EXPENSES
            ]),
            width="100%", variant="surface",
        ),
        overflow_x="auto", width="100%",
    )


def overview() -> rx.Component:
    return rx.vstack(
        rx.grid(
            kpi("Gasto total", "1.248,50 €", "Suma de los 4 ejemplos", "wallet"),
            kpi("Gastos registrados", "4", "Registros ficticios", "receipt"),
            kpi("Gasto promedio", "312,13 €", "Promedio por registro", "calculator"),
            kpi("Mayor categoría", "Vivienda", "620,00 € en los ejemplos", "house"),
            columns=rx.breakpoints(initial="1", sm="2", lg="4"), spacing="4", width="100%",
        ),
        pending("KPIs de ejemplo. Falta calcularlos con datos del usuario.",
                "services.py: expense_summary · state.py: cargar indicadores · ui_preview.py: tarjetas"),
        rx.grid(
            panel(
                "¿En qué se va el dinero?", "Gasto por categoría · demostración (€)",
                rx.recharts.bar_chart(
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
                    rx.recharts.x_axis(data_key="categoria", tick={"fontSize": 11}, interval=0),
                    rx.recharts.y_axis(width=45), rx.recharts.graphing_tooltip(),
                    rx.recharts.bar(data_key="importe", fill="#0d9488", radius=[5, 5, 0, 0]),
                    data=CATEGORY_DATA, width="100%", height=260,
                ),
                pending("Falta agrupar los gastos por categoría con Pandas.",
                        "services.py: expense_summary · state.py · ui_preview.py: gráficos"),
            ),
            panel(
                "Tu gasto en el tiempo", "Septiembre y octubre de 2026 · demostración (€)",
                rx.recharts.bar_chart(
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
                    rx.recharts.x_axis(data_key="mes"), rx.recharts.y_axis(width=45),
                    rx.recharts.graphing_tooltip(),
                    rx.recharts.bar(data_key="importe", fill="#6366f1", radius=[5, 5, 0, 0]),
                    data=MONTH_DATA, width="100%", height=260,
                ),
                pending("Falta agrupar por mes y conectar los filtros.",
                        "services.py: expense_summary · state.py · ui_preview.py: gráficos"),
            ),
            columns=rx.breakpoints(initial="1", lg="2"), spacing="5", width="100%",
        ),
        panel(
            "Movimientos de ejemplo", "Estos registros no existen en SQLite.", expense_table(),
            pending("Falta consultar, editar y confirmar la eliminación de gastos.",
                    "services.py: list_expenses / update_expense / delete_expense · state.py"),
        ),
        spacing="5", width="100%", align="stretch",
    )


def field(label: str, component: rx.Component) -> rx.Component:
    return rx.vstack(rx.text(label, size="2", weight="medium"), component,
                     spacing="2", align="stretch", width="100%")


def expenses() -> rx.Component:
    return rx.vstack(
        rx.grid(
            panel(
                "Nuevo gasto", "Vista previa del formulario. Los controles todavía están deshabilitados.",
                field("Descripción", rx.input(placeholder="Ej. Compra semanal", disabled=True, width="100%")),
                rx.grid(
                    field("Importe (€)", rx.input(type="number", placeholder="0,00", disabled=True)),
                    field("Fecha", rx.input(type="date", disabled=True)),
                    columns=rx.breakpoints(initial="1", sm="2"), spacing="4",
                ),
                field("Categoría", rx.select(
                    ["Alimentación", "Transporte", "Vivienda", "Salud", "Educación", "Ocio", "Compras", "Servicios", "Otros"],
                    placeholder="Seleccionar categoría", disabled=True, width="100%",
                )),
                rx.button(rx.icon("plus", size=16), "Guardar gasto · pendiente", disabled=True),
                pending("Falta capturar el formulario y guardar el gasto validado.",
                        "schemas.py: ExpenseCreate / ExpenseUpdate · state.py · services.py: create_expense"),
            ),
            panel(
                "Buscar y filtrar", "Los filtros serán aplicados a los gastos del usuario autenticado.",
                field("Buscar descripción", rx.input(placeholder="Buscar un gasto…", disabled=True)),
                field("Categoría", rx.select(["Todas"], default_value="Todas", disabled=True)),
                rx.grid(
                    field("Desde", rx.input(type="date", disabled=True)),
                    field("Hasta", rx.input(type="date", disabled=True)),
                    columns=rx.breakpoints(initial="1", sm="2"), spacing="4",
                ),
                pending("Falta añadir parámetros de filtrado al servicio y al estado.",
                        "services.py: ampliar list_expenses · state.py: búsqueda y fechas"),
                rx.separator(),
                rx.heading("Excel", size="3"),
                rx.flex(
                    rx.button("Importar Excel", variant="soft", disabled=True),
                    rx.button("Exportar Excel", variant="soft", disabled=True),
                    gap="12px", flex_wrap="wrap",
                ),
                pending("Falta implementar subida, validación y descarga de Excel.",
                        "services.py: import_excel / export_excel · schemas.py · state.py"),
            ),
            columns=rx.breakpoints(initial="1", lg="2"), spacing="5", width="100%",
        ),
        panel(
            "Listado de gastos", "Tabla de demostración; acciones deshabilitadas.", expense_table(),
            pending("La eliminación necesitará confirmación antes de llamar al servicio.",
                    "ui_preview.py: diálogo · state.py: confirmar borrado · services.py: delete_expense"),
        ),
        spacing="5", width="100%", align="stretch",
    )


def access() -> rx.Component:
    return rx.grid(
        panel(
            "Acceder a tu cuenta", "Maqueta de acceso. No introduce ni valida credenciales.",
            field("Usuario", rx.input(placeholder="Nombre de usuario", disabled=True)),
            field("Contraseña", rx.input(type="password", placeholder="Contraseña", disabled=True)),
            rx.button("Entrar · pendiente", disabled=True),
            pending("Falta verificar la contraseña y establecer la sesión en el servidor.",
                    "schemas.py: UserLogin · services.py: authenticate_user · state.py: login/logout y _user_id"),
        ),
        panel(
            "Crear cuenta", "El registro también está pendiente de conexión.",
            field("Usuario", rx.input(placeholder="Nombre de usuario", disabled=True)),
            field("Email", rx.input(type="email", placeholder="tu@email.com", disabled=True)),
            field("Contraseña", rx.input(type="password", placeholder="Contraseña", disabled=True)),
            rx.button("Registrarme · pendiente", disabled=True, variant="soft"),
            pending("Falta guardar un hash seguro, controlar duplicados y cargar datos iniciales.",
                    "schemas.py: UserCreate · services.py: register_user · seed.py · models.py: User"),
        ),
        columns=rx.breakpoints(initial="1", lg="2"), spacing="5", width="100%",
    )


def roadmap() -> rx.Component:
    return rx.vstack(
        panel(
            "Gantt · Plan de trabajo del equipo",
            "Propuesta de dos jornadas de ocho horas. Pulsa la imagen para ampliarla; ajustar el plazo según aprendizaje e integración.",
            rx.link(
                rx.image(
                    src="/gantt_control_gastos.png",
                    alt="Gantt de Control de Gastos: Dimitry, Sanjana, Lindey, Gustavo y Matheus; tareas paralelas, integración y revisión conjunta en dos jornadas.",
                    width="100%", height="auto", border_radius="8px",
                ),
                href="/gantt_control_gastos.png", is_external=True,
                aria_label="Abrir el Gantt de Control de Gastos a tamaño completo",
            ),
        ),
        panel(
            "Cómo vamos a repartir el trabajo",
            "Entregas pequeñas para aprender juntos. La carga se revisará tras la primera entrega; los nombres de rama son propuestas.",
            rx.callout(
                "Todo sigue pendiente de implementación funcional. Este plan asigna responsabilidades; no habilita login, CRUD ni permisos de GitHub.",
                icon="info", color_scheme="teal",
            ),
            rx.vstack(*[rx.text(step, size="2") for step in DELIVERY_ORDER], spacing="3", align="stretch"),
        ),
        *[
            panel(
                f"{item['owner']} · {item['area']}",
                "Responsable del bloque · Rutas relativas a ControlGastos/gestion_gastos/.",
                rx.badge("PENDIENTE · ENTREGAS POR FASES", color_scheme=item["color"]),
                rx.vstack(*[rx.text(delivery, size="2") for delivery in item["deliveries"]], spacing="3", align="stretch"),
                *[
                    rx.vstack(
                        rx.text(label, size="2", weight="bold"),
                        rx.text(item[key], size="2", color="#475569", overflow_wrap="anywhere"),
                        spacing="1", align="stretch",
                    ) for label, key in [
                        ("Alcance", "scope"),
                        ("Restricciones", "restrictions"),
                        ("Coordinación y observaciones", "coordination"),
                    ]
                ],
                pending("Funciones y archivos de referencia", item["files"]),
                pending("Git y forma de entrega", item["git"]),
            ) for item in RESPONSIBILITIES
        ],
        panel(
            "Acuerdos compartidos de Git e integración",
            "Propuesta de trabajo del equipo. Las protecciones del repositorio no se cambian desde esta pantalla.",
            rx.vstack(*[
                rx.hstack(
                    rx.badge(str(index), color_scheme="gray"),
                    rx.text(agreement, size="2"), align="start", spacing="3",
                ) for index, agreement in enumerate(TEAM_AGREEMENTS, start=1)
            ], spacing="4", align="stretch"),
        ),
        spacing="5", width="100%", align="stretch",
    )


def dashboard() -> rx.Component:
    return rx.box(
        rx.box(
            rx.flex(
                rx.hstack(
                    rx.box(rx.icon("wallet", size=24, color="white"), background="#0d9488", padding="10px", border_radius="12px"),
                    rx.vstack(
                        rx.heading("ControlGastos", size="5"),
                        rx.text("GESTIÓN DE GASTOS PERSONALES", size="1", color="#64748b"),
                        spacing="1", align="start",
                    ), align="center", spacing="3",
                ),
                rx.badge("MAQUETA · DATOS FICTICIOS", color_scheme="amber", size="2"),
                justify="between", align="center", flex_wrap="wrap", gap="16px",
                max_width="1280px", margin="0 auto",
            ),
            padding=["20px", "24px 36px"], background="white", border_bottom="1px solid #e2e8f0",
        ),
        rx.vstack(
            rx.box(
                rx.text("UNA VISIÓN CLARA DE TUS FINANZAS", size="1", weight="bold", color="#0d9488"),
                rx.heading("Cada gasto, en su sitio.", size="8", margin_top="10px", color="#0f172a"),
                rx.text("Explora la interfaz propuesta y consulta qué falta conectar en cada sección.",
                        color="#64748b", margin_top="10px"),
            ),
            rx.callout(
                "Vista previa académica. No hay sesión iniciada ni conexión a SQLite. Los importes y gráficos son ejemplos; ninguna acción guarda datos.",
                icon="info", color_scheme="amber", width="100%",
            ),
            rx.tabs.root(
                rx.box(
                    rx.tabs.list(
                        rx.tabs.trigger("Resumen", value="overview"),
                        rx.tabs.trigger("Gastos", value="expenses"),
                        rx.tabs.trigger("Acceso", value="access"),
                        rx.tabs.trigger("Qué falta implementar", value="roadmap"),
                    ), overflow_x="auto", margin_bottom="24px",
                ),
                rx.tabs.content(overview(), value="overview"),
                rx.tabs.content(expenses(), value="expenses"),
                rx.tabs.content(access(), value="access"),
                rx.tabs.content(roadmap(), value="roadmap"),
                default_value="overview", width="100%",
            ),
            rx.text("Prototipo visual · Sin persistencia ni autenticación funcional", size="1", color="#64748b"),
            spacing="6", align="stretch", width="100%", max_width="1280px",
            margin="0 auto", padding=["24px 16px", "36px"],
        ),
        min_height="100vh", background="#f1f5f9", color="#0f172a",
    )
