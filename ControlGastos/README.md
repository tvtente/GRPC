# Gestión de Gastos Personales · ControlGastos

## Arquitectura aprobada

Este esqueleto sigue el PDF de estructura: Reflex → estado → validación Pydantic
→ servicios → SQLAlchemy → SQLite. Pandas hará el análisis; OpenPyXL permitirá
importar y exportar Excel. **SQLite será la fuente de datos**, no `gastos.xlsx`.
Esta decisión sustituye expresamente el alcance inicial de Excel sin login.

## Estado actual: Fase 2

Preparados: dependencias, módulos, tablas SQLAlchemy, contratos Pydantic,
infraestructura de sesiones, configuración Alembic, migración inicial y página de
comprobación del estado Reflex. La migración se verificó en una base temporal;
no se ha creado la base personal `data/gastos.db`.

Pendientes: registro, hash/verificación de contraseñas, login/logout, carga inicial,
CRUD, filtros, análisis, importación/exportación y sus pantallas. Las funciones de
servicio pendientes lanzan `NotImplementedError`: no simulan éxito ni guardan datos.
La página actual no es una pantalla de login ni un gestor de gastos terminado.

## Estructura y responsabilidades

```text
ControlGastos/
├── rxconfig.py
├── pyproject.toml             # Dependencias gestionadas con uv
├── uv.lock                    # Versiones reproducibles
├── requirements.txt           # Exportado desde uv.lock
├── alembic.ini
├── README.md
├── alembic/
│   ├── env.py                 # Misma URL y metadatos que la aplicación
│   ├── script.py.mako         # Plantilla para próximas migraciones
│   └── versions/
│       └── 0001_tablas_iniciales.py
├── gestion_gastos/
│   ├── __init__.py
│   ├── database.py            # Engine, Base, claves foráneas y get_session
│   ├── models.py              # User, Category, Expense y relaciones
│   ├── schemas.py             # Entrada validada y salida sin contraseñas
│   ├── services.py            # Interfaces de auth, CRUD, Pandas y Excel
│   ├── seed.py                # Interfaz de carga inicial, todavía pendiente
│   ├── state.py               # Estado Reflex y evento de comprobación
│   ├── work_plan.py           # Responsables, alcance y acuerdos de Git
│   ├── ui_preview.py          # Maqueta de dashboard con avisos por sección
│   └── gestion_gastos.py      # App y registro de la página
└── data/
    └── .gitkeep               # Directorio de gastos.db y archivos locales
```

Se conserva `gestion_gastos` en lugar de renombrarlo a `gastos_app`, para mantener
la configuración y el paquete existentes. El nombre exterior es `ControlGastos`.
Se sigue usando uv; `requirements.txt` es una exportación para quienes usen pip.
No editarlo a mano: actualizar dependencias con uv y volver a exportar.

## Preparar y arrancar

Desde la raíz de ProjeCTC:

```bash
uv sync --directory ControlGastos
uv run --directory ControlGastos reflex run
```

Abrir <http://localhost:3002>; backend en 8002. La maqueta muestra pestañas de
Resumen, Gastos, Acceso y Qué falta implementar. Los KPIs, gráficos y filas son
ficticios; formularios y acciones están deshabilitados. Cada bloque indica qué
falta conectar y en qué módulos. No consulta la base ni inicia sesión.
Ctrl+C detiene el servidor.

### Alternativa con entorno virtual y pip

Necesitas Python 3.13 o posterior. Desde la carpeta `ControlGastos`:

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m reflex run
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m reflex run
```

Si utilizas pip, para aplicar la migración desde el entorno activo ejecuta
`python -m alembic upgrade head`. Para la maqueta no hace falta crear la base.

Para generar las tablas cuando se quiera preparar la base local:

```bash
cd ControlGastos
uv run alembic upgrade head
uv run alembic current
```

Ya existe la revisión inicial; no hay que volver a generarla. `upgrade head`
creará `ControlGastos/data/gastos.db` y las tablas. La ruta se calcula desde el
proyecto. `GASTOS_DATABASE_URL` permite usar otra base, por ejemplo una temporal.
Importar módulos no crea tablas; se usa Alembic, no `create_all` en el arranque.

Cuando cambien modelos en fases posteriores, desde `ControlGastos`:

```bash
uv run alembic revision --autogenerate -m "describir el cambio"
# Revisar la migración generada antes de aplicarla.
uv run alembic upgrade head
```

## Contratos y colaboración

- `models.py`: relaciones users 1:N expenses y categories 1:N expenses; importe
  decimal positivo y borrado de gastos en cascada al borrar su usuario.
- `schemas.py`: UserCreate, UserLogin, UserRead, ExpenseCreate, ExpenseUpdate,
  ExpenseRead y CategoryRead. Valida email, contraseña, descripción, fecha no
  futura, importe positivo con un máximo de dos decimales y categoría positiva.
  ExpenseUpdate representa un formulario completo, no un parche parcial.
- `services.py`: cada operación de gastos recibe `user_id` desde la sesión del
  servidor; deberá comprobar propietario y categoría existente al implementarse.
  Los esquemas de entrada rechazan campos extra, incluido un user_id del cliente.
- `state.py`: `_user_id` es un campo privado del backend reservado para login;
  todavía no se asigna ni se usa como una autenticación funcional.
- `seed.py`: conserva las categorías del ejercicio. La creación de administrador
  recibirá credenciales explícitas y usará el servicio de registro; no se añade
  una contraseña fija a Git. Las funciones todavía no están implementadas.

El PDF propone admin/admin1234; aquí no se crea ese usuario automáticamente.
La contraseña deberá llegar por configuración o entrada explícita cuando se
implemente el seed. El guardado seguro del hash está pendiente con el login.

## Comprobaciones realizadas

- Imports de los módulos y compilación de la página con `reflex compile --dry`.
- Migración inicial y `alembic check` en SQLite temporal.
- Claves foráneas activas y eliminación en cascada.
- Rechazo de importe cero, exceso de decimales y user_id en un formulario.
- Validación básica de UserCreate.

Estas comprobaciones no certifican login, CRUD o aislamiento por usuario:
son funcionalidades pendientes. Confirmar la Fase 2 antes de implementarlas.

## Errores comunes

- Módulo no encontrado: ejecutar `uv sync` y usar `uv run` con la carpeta correcta.
- Puerto ocupado: liberar 3002/8002 o actualizar conjuntamente los puertos y URLs
  de `rxconfig.py`.
- `no such table`: aplicar `uv run alembic upgrade head` cuando se habiliten los
  servicios; la página del esqueleto no necesita acceder a tablas.
- `NotImplementedError`: se ha llamado a una interfaz pendiente; no es un fallo
  de instalación ni una operación que se haya guardado parcialmente.

Datos SQLite, archivos Excel, entornos y compilados se excluyen de Git.

## Documentación técnica

- SQLAlchemy: https://docs.sqlalchemy.org/en/20/orm/declarative_config.html
- Alembic: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- Pydantic: https://docs.pydantic.dev/latest/concepts/validators/

## Maqueta visual y próximos enlaces

`ui_preview.py` contiene únicamente presentación y ejemplos estáticos. Cambiar
los textos o el diseño no debe introducir consultas SQL en este módulo.

| Sección | Implementación pendiente |
| --- | --- |
| Registro/login | `services.py`: registro, hash y autenticación; `state.py`: eventos y sesión; `schemas.py`: validación |
| Tabla y acciones | `services.py`: listado, edición y eliminación por propietario; `state.py`: recarga; `ui_preview.py`: confirmación |
| Formulario | `state.py`: captura y envío; `services.py`: create_expense; `schemas.py`: ExpenseCreate |
| Filtros | `services.py`: extender list_expenses; `state.py`: categoría y rango de fechas |
| Indicadores y gráficos | `services.py`: expense_summary con Pandas; `state.py`: variables derivadas; `ui_preview.py`: datos reactivos |
| Excel | `services.py`: import_excel/export_excel; `state.py`: subida y descarga |

La navegación entre pestañas funciona, pero no representa un CRUD o login
implementado. Los ejemplos no se escriben en SQLite ni en Excel.

## Responsabilidades del equipo

La pestaña «Qué falta implementar» presenta el reparto mantenido en
`gestion_gastos/work_plan.py`: Dimitry (base y acceso), Sanjana (CRUD por entregas),
Lindey (categorías y selector), Gustavo (filtros, KPIs e integración) y Matheus
(Excel: exportación antes de importación). Cada bloque incluye alcance,
restricciones, dependencias, funciones de referencia y propuesta de trabajo Git.
El panel no crea ramas ni modifica permisos. Revisar la carga tras la primera
entrega y acordar firmas de funciones para evitar conflictos en archivos compartidos.
