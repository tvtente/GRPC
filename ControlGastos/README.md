# Gestión de Gastos Personales

Aplicación académica independiente dentro de `ControlGastos`, gestionada con `uv`.
Usará Python, Reflex, Pandas y OpenPyXL. La persistencia será exclusivamente
`ControlGastos/data/gastos.xlsx`: sin SQL, autenticación ni arquitectura multiusuario.

## Fase 1: preparar y comprobar el entorno

El objetivo de esta fase es comprobar el entorno y abrir una página mínima.
No incluye todavía CRUD, estados de formularios, Excel, filtros, KPIs ni gráficos.
No avanzar a la Fase 2 hasta confirmar que esta página funciona en el navegador.

Se verificó Reflex 0.10.1 en el proyecto existente y se fijó esa misma versión
en este entorno para mantener sintaxis reproducible. Python requerido: 3.13 o posterior.
`uv.lock` fija también las dependencias transitivas.

Desde la raíz de ProjeCTC:

```bash
uv sync --directory ControlGastos
uv run --directory ControlGastos reflex run
```

También se puede ejecutar desde esta carpeta:

```bash
uv sync
uv run reflex run
```

Abrir <http://localhost:3002>. El backend utiliza el puerto 8002.
Resultado esperado: título «Gestión de Gastos Personales», etiqueta
«FASE 1 · ENTORNO PREPARADO» y aviso de que el registro se construirá después.
Detener el servidor con Ctrl+C.

## Archivos de esta fase

- `pyproject.toml`: nombre, versión de Python y dependencias.
- `uv.lock`: versiones reproducibles, gestionadas por uv.
- `.python-version`: Python 3.13 para uv.
- `rxconfig.py`: nombre del módulo y puertos independientes.
- `gestion_gastos/__init__.py`: identifica el paquete Python.
- `gestion_gastos/gestion_gastos.py`: construye la página y registra la ruta `/`.
- `.gitignore`: excluye entornos, compilados y los futuros datos personales de Excel.

`rx.Config` configura el proyecto. `index()` devuelve componentes visuales.
`rx.App` crea la aplicación y `add_page` registra la página inicial.
El nombre de la carpeta exterior es `ControlGastos`, como se solicitó; el paquete
interior se llama `gestion_gastos`, siguiendo la arquitectura propuesta.

## Errores comunes

- `uv: command not found`: uv debe estar instalado y disponible en la terminal.
- Módulo `reflex` no encontrado: ejecutar `uv sync` y usar `uv run` desde esta
  carpeta o indicar `--directory ControlGastos` desde la raíz.
- Puerto ocupado: cerrar la otra instancia que utiliza 3002/8002. Si se cambian
  puertos, actualizar también `api_url` y `deploy_url` en `rxconfig.py`.
- Primera ejecución lenta o fallo de descarga: Reflex prepara el frontend y puede
  necesitar conexión para instalar sus herramientas y dependencias.

## Fases siguientes (pendientes)

2. Estructura modular de carpetas y archivos.
3. Servicio Excel y creación de `data/gastos.xlsx`.
4. Pruebas independientes de lectura y CRUD.
5. Estado Reflex.
6. Tabla de gastos.
7. Formulario de registro.
8. Edición y eliminación con confirmación.
9. Filtros y búsqueda.
10. KPIs y análisis con Pandas.
11. Gráficos.
12. Revisión de validaciones y manejo de errores.
13. Pruebas generales y preparación de la presentación.

Cada fase se explicará y comprobará antes de avanzar. Los módulos de servicios
serán los únicos que accedan al Excel; la interfaz se comunicará con ellos a
través del estado. El archivo Excel se creará en la Fase 3, no en esta fase.
