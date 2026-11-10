"""Acuerdos de trabajo mostrados en la maqueta; no son permisos de GitHub."""

RESPONSIBILITIES = [
    {
        "owner": "Dimitry", "color": "blue", "area": "Base de datos y acceso",
        "deliveries": [
            "1. Aplicar la migración en una base local y preparar un usuario de prueba para que el equipo pueda avanzar.",
            "2. Implementar registro, hash/verificación de contraseña, login y logout; establecer la identidad en el servidor.",
        ],
        "scope": "Entregar conexión, sesión y datos de prueba; después completar autenticación. No asumir el CRUD ni los gráficos.",
        "restrictions": "No cambiar nombres de tablas o contratos compartidos sin acordarlo. No guardar contraseñas en claro ni aceptar el propietario desde el formulario.",
        "coordination": "Publicar instrucciones breves de arranque y cómo obtener el usuario autenticado. Mantener estable ese contrato para Sanjana y Matheus.",
        "files": "database.py · models.py · schemas.py: UserCreate / UserLogin / UserRead · services.py: register_user / authenticate_user · seed.py: seed_admin · state.py: sesión · ../alembic/",
        "git": "Rama sugerida: dimitry/base-acceso. PR de base y migración primero; PR de autenticación después. Revisar con Gustavo los cambios de esquema.",
    },
    {
        "owner": "Sanjana", "color": "violet", "area": "CRUD sencillo de gastos",
        "deliveries": [
            "1. Registrar y consultar gastos con descripción, importe, fecha y categoría usando datos correctos de ejemplo.",
            "2. Editar el gasto por su ID y eliminarlo con confirmación sencilla; recargar la tabla después de cada operación.",
        ],
        "scope": "Aprender el recorrido interfaz → estado → servicio → base. Primera entrega sin filtros, gráficos ni nuevas validaciones de negocio complejas.",
        "restrictions": "Conservar esquemas y restricciones existentes. Identificar cada gasto por ID y filtrar siempre por el usuario del servidor; no usar SQL desde la interfaz.",
        "coordination": "Recibir de Dimitry el usuario de prueba y de Lindey las categorías. Entregar ejemplos escritos de entrada/salida; si el login está pendiente, probar el servicio con el usuario de prueba desde el servidor.",
        "files": "services.py: list_expenses / get_expense / create_expense / update_expense / delete_expense · state.py: eventos CRUD · ui_preview.py: formulario, tabla y confirmación · schemas.py: usar ExpenseCreate / ExpenseUpdate / ExpenseRead",
        "git": "Rama sugerida: sanjana/crud-gastos. PR pequeño para crear/consultar y otro para editar/eliminar. Acordar las funciones compartidas antes de modificarlas.",
    },
    {
        "owner": "Lindey", "color": "pink", "area": "Categorías y selector",
        "deliveries": [
            "1. Cargar las categorías iniciales sin duplicarlas y ofrecer su listado mediante el servicio.",
            "2. Sustituir las opciones ficticias por categorías reales en el formulario; conservar el ID al crear y editar.",
        ],
        "scope": "Categorías, carga inicial, selector y aviso de selección pendiente. No crear todavía una pantalla completa de mantenimiento de categorías.",
        "restrictions": "No renombrar o borrar categorías usadas por gastos. No crear otra tabla ni un estado paralelo con SQL propio; reutilizar Category y CategoryRead.",
        "coordination": "Acordar con Sanjana cómo recibe y envía category_id. Acordar con Matheus cómo se traducen los nombres de categoría del Excel.",
        "files": "seed.py: seed_categories · services.py: list_categories · state.py: categorías y selección · ui_preview.py: selector · models.py: usar Category · schemas.py: usar CategoryRead",
        "git": "Rama sugerida: lindey/categorias. Practicar commit y push con acompañamiento de Gustavo; revisar el diff antes del PR. No entregar carpetas duplicadas de la aplicación.",
    },
    {
        "owner": "Gustavo", "color": "teal", "area": "Filtros, KPIs e integración",
        "deliveries": [
            "1. Acordar interfaces, revisar PRs y acompañar los ajustes de Git. Conectar categoría, búsqueda y rango de fechas cuando funcione el listado.",
            "2. Calcular total, cantidad, promedio y mayor categoría con Pandas; conectar gráficos por categoría y mes.",
        ],
        "scope": "Coordinar contratos e integrar entregas pequeñas. Priorizar integración y filtros; completar KPIs y gráficos después para no concentrar toda la carga al inicio.",
        "restrictions": "No rehacer aportes ajenos sin explicar el cambio y conservar autoría. No mezclar refactorizaciones generales con una entrega funcional.",
        "coordination": "Revisar con cada responsable sus propios cambios. Aplicar los mismos filtros a tabla, indicadores y gráficos; cada integrante comprueba su entrega.",
        "files": "services.py: parámetros de list_expenses y expense_summary · state.py: filtros e indicadores · ui_preview.py: filtros, tarjetas y gráficos",
        "git": "Rama sugerida: gustavo/filtros-kpis. Mantener PRs de integración pequeños y coordinar conflictos en archivos compartidos sin sobrescribir el trabajo de otra persona.",
    },
    {
        "owner": "Matheus", "color": "orange", "area": "Excel: exportación e importación",
        "deliveries": [
            "1. Exportar los gastos del usuario a un Excel tabular con encabezados acordados y descarga desde la interfaz.",
            "2. Importar un archivo de ejemplo del mismo formato: revisar filas, resolver categorías y mostrar un resumen antes de guardar.",
        ],
        "scope": "Exportación primero para aprender el flujo; importación después. Empezar con un archivo y formato conocidos, no con cualquier hoja Excel.",
        "restrictions": "SQLite sigue siendo la fuente principal. No importar user_id del archivo ni sobrescribir registros existentes; una importación inválida no debe dejar un guardado parcial.",
        "coordination": "Acordar columnas con Gustavo y categorías con Lindey. Reutilizar validaciones y servicios de gastos; antes de importar, explicar cómo se tratarán reimportaciones y duplicados.",
        "files": "services.py: export_excel / import_excel · schemas.py: usar ExpenseCreate · state.py: subida, descarga y resumen · ui_preview.py: controles Excel",
        "git": "Rama sugerida: matheus/excel. Primer PR solo de exportación; segundo de importación. Acompañamiento de Gustavo en Git y exclusión de archivos con datos personales.",
    },
]

TEAM_AGREEMENTS = [
    "Primero funcionamiento sencillo con datos correctos; después mensajes, casos límite y validaciones adicionales. No retirar las restricciones o validaciones ya existentes para facilitar una demostración.",
    "Cada responsable comprueba su propia entrega y explica cómo repetirla. La revisión conjunta se hace antes de integrar; no recae toda sobre Gustavo.",
    "services.py, state.py y ui_preview.py son compartidos: asignar funciones y secciones, no exclusividad del archivo. Avisar antes de cambiar una firma o mover código.",
    "Las ramas propuestas son orientativas: aprovechar las ramas existentes y acordar nombres antes de crear otras. Este panel no crea ramas ni modifica permisos.",
    "Sincronizar con main antes de empezar y antes del PR. Si hay cambios locales, guardarlos de forma segura; evitar reset --hard y push forzado como solución de conflictos.",
    "Revisar git status y git diff antes de añadir archivos. Commit local → prueba → push a la rama personal cuando se autorice → PR revisado → merge acordado a main.",
    "No subir .venv, .web, gastos.db, contraseñas, Excel personales ni carpetas de comparación. Conservar comentarios de autoría y explicar adaptaciones en el commit/PR.",
]

DELIVERY_ORDER = [
    "1 · Base y datos de prueba (Dimitry) + categorías (Lindey). Acordar contratos de usuario y categoría.",
    "2 · Crear y consultar (Sanjana). Completar acceso (Dimitry) y conectar selector (Lindey).",
    "3 · Editar/eliminar (Sanjana), filtros (Gustavo) y exportación Excel (Matheus).",
    "4 · KPIs y gráficos (Gustavo), importación Excel (Matheus) y revisión conjunta de casos límite.",
]
