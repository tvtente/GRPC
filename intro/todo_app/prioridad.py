"""Controles y niveles de prioridad de Lindey, adaptados al estado compartido.

La interfaz conserva selectores y colores. El estado y el repositorio gestionan
la persistencia para guardar cada tarea y su prioridad en la misma transacción.

Procedencia: Lindey aportó niveles, colores, selección obligatoria, controles
de creación/edición y prioridad Media para tareas anteriores. Esta versión
adapta esas funciones; no es una copia literal de su archivo original.
La redistribución está documentada en las observaciones del commit de integración.
"""

# APORTE DE LINDEY: niveles disponibles y valor para tareas anteriores.
PRIORIDADES = ['Baja', 'Media', 'Alta', 'Urgente']
POR_DEFECTO = 'Media'


def _selector(valor, al_cambiar):
    # ADAPTACIÓN EN GUSTAVO: recibe valor y evento de TodoState;
    # sustituye la dependencia del PrioridadState separado del original.
    import reflex as rx

    return rx.vstack(
        rx.hstack(
            rx.icon('flag', size=16), rx.text('Prioridad', weight='bold'),
            align='center', gap='6px',
        ),
        rx.select(
            PRIORIDADES, value=valor, on_change=al_cambiar,
            placeholder='Elija su prioridad', aria_label='Prioridad',
            width='100%', size='3',
        ),
        align='start', gap='8px', width='100%', min_width='0',
    )


def prioridad_formulario(valor, al_cambiar):
    """Control de creación de Lindey conectado al estado compartido."""
    return _selector(valor, al_cambiar)


def prioridad_edicion(valor, al_cambiar):
    """Control de edición de Lindey conectado al estado compartido."""
    return _selector(valor, al_cambiar)


def prioridad_control(nivel):
    # APORTE DE LINDEY: etiqueta y colores. La prioridad llega desde TodoView,
    # en lugar de consultarse en un diccionario de un segundo estado.
    import reflex as rx

    color = rx.match(
        nivel, ('Baja', 'gray'), ('Media', 'blue'),
        ('Alta', 'orange'), ('Urgente', 'red'), 'blue',
    )
    return rx.flex(
        rx.text('Prioridad:', size='2', color='#94a3b8'),
        rx.badge(nivel, color_scheme=color), align='center', gap='8px',
    )
