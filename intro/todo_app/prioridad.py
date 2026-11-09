"""Prioridad de las tareas, aparte del código principal.

Usa la columna prioridad de la tabla todos. Si la columna no existe, la crea
ella misma, sin depender de init_database.
"""
import reflex as rx
from sqlalchemy import text

from .database import get_engine

PRIORIDADES = ['Baja', 'Media', 'Alta', 'Urgente']
POR_DEFECTO = 'Media'


def _asegurar_columna():
    """Añade la columna prioridad a todos si todavía no está."""
    with get_engine().begin() as con:
        columnas = con.execute(text('PRAGMA table_info(todos)')).mappings().all()
        if 'prioridad' not in {c['name'] for c in columnas}:
            con.execute(text("ALTER TABLE todos "
                             "ADD COLUMN prioridad TEXT NOT NULL DEFAULT 'Media'"))


class PrioridadState(rx.State):
    niveles: dict[int, str] = {}
    nueva: str = POR_DEFECTO   # lo que está elegido en el formulario
    ultimo_id: int = -1        # mayor id conocido, sirve para detectar la tarea nueva

    @rx.event
    def cargar(self):
        _asegurar_columna()
        with get_engine().connect() as con:
            filas = con.execute(text('SELECT id, prioridad FROM todos')).all()
        self.niveles = {fila[0]: fila[1] for fila in filas}
        self.ultimo_id = max(self.niveles, default=0)

    @rx.event
    def set_nueva(self, nivel: str):
        if nivel in PRIORIDADES:
            self.nueva = nivel

    @rx.event
    def aplicar_nueva(self):
        """Se ejecuta después de añadir: da la prioridad elegida a la tarea nueva."""
        if self.ultimo_id < 0:
            return
        with get_engine().begin() as con:
            resultado = con.execute(
                text('UPDATE todos SET prioridad = :nivel WHERE id > :ultimo'),
                {'nivel': self.nueva, 'ultimo': self.ultimo_id})
        self.cargar()
        if resultado.rowcount > 0:   # solo se reinicia si de verdad se creó una tarea
            self.nueva = POR_DEFECTO

    @rx.event
    def cambiar(self, todo_id: int, nivel: str):
        if nivel not in PRIORIDADES:
            return
        _asegurar_columna()
        with get_engine().begin() as con:
            con.execute(text('UPDATE todos SET prioridad = :nivel WHERE id = :id'),
                        {'nivel': nivel, 'id': todo_id})
        self.niveles = {**self.niveles, todo_id: nivel}


def _nivel(todo_id):
    """Prioridad de una tarea; si no tiene, la de por defecto."""
    return rx.cond(PrioridadState.niveles.contains(todo_id),
                   PrioridadState.niveles[todo_id], POR_DEFECTO)


def prioridad_formulario():
    """Selector para el formulario de crear tarea, antes de pulsar Añadir."""
    return rx.vstack(
        rx.hstack(rx.icon('flag', size=16), rx.text('Prioridad', weight='bold'),
                  align='center', gap='6px'),
        rx.select(PRIORIDADES, value=PrioridadState.nueva,
                  on_change=PrioridadState.set_nueva,
                  aria_label='Prioridad', width='100%', size='3'),
        align='start', gap='6px', width='50%', margin_left='auto')


def prioridad_control(todo_id):
    """En cada tarea guardada: solo muestra la prioridad elegida."""
    nivel = _nivel(todo_id)
    color = rx.match(nivel,
                     ('Baja', 'gray'),
                     ('Media', 'blue'),
                     ('Alta', 'orange'),
                     ('Urgente', 'red'),
                     'blue')
    return rx.flex(
        rx.text('Prioridad:', size='2', color='#94a3b8'),
        rx.badge(nivel, color_scheme=color),
        align='center', gap='8px')

# Agregar estas lineas a todo_app.py:
# 1. Debajo de los import:
# from .prioridad import PrioridadState, prioridad_control, prioridad_formulario
# 2. todo_item, dentro del rx.vstack, justo debajo de la línea rx.text('Creado: ', ...):
# prioridad_control(todo.id),
# 3. En todo_form, entre el rx.text_area(...) y el botón Añadir tarea:
# prioridad_formulario(),
# 4. En el on_submit del mismo formulario, para que después de añadir se aplique la prioridad:
# on_submit=lambda _:[TodoState.add_todo(),PrioridadState.aplicar_nueva()]
# 5. La última línea, con PrioridadState.cargar en el on_load:
# app.add_page(index,title='Lista de tareas · CRUD Reflex',on_load=[TodoState.load_todos,PrioridadState.cargar])
