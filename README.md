# GRPC

Proyecto Reflex con Python, gestionado con `uv`. La aplicación de la raíz comienza con una página vacía para construir el proyecto.

## Instalar y ejecutar

Necesitas Python 3.13 o posterior y `uv`.

```bash
uv sync
uv run reflex run
```

Abre <http://localhost:3000>. El backend utiliza el puerto 8000.

## Estructura

- `grpc/grpc.py`: aplicación y página inicial vacía.
- `rxconfig.py`: configuración de Reflex.
- `pyproject.toml` y `uv.lock`: dependencias y versiones reproducibles.
- [`intro/`](intro/): base de referencia con el ejemplo CRUD, pruebas y documentación; conserva su configuración independiente.

Los entornos virtuales, archivos generados, credenciales y bases de datos locales se excluyen de Git.
