"""Engine propio: SQLite local por defecto, sin modificar la configuración de otros ejercicios."""
from functools import lru_cache
from pathlib import Path
import os
from sqlmodel import SQLModel, create_engine, text

PROJECT = Path(__file__).resolve().parents[1]

@lru_cache(maxsize=1)
def get_engine():
    url = os.environ.get('TODO_DATABASE_URL')
    if not url:
        path = PROJECT / 'data' / 'todos.db'
        path.parent.mkdir(parents=True, exist_ok=True)
        url = f'sqlite:///{path}'
    options = {'check_same_thread': False, 'timeout': 10} if url.startswith('sqlite:') else {}
    return create_engine(url, connect_args=options)

def init_database(engine=None):
    from .models import Todo
    eng = engine if engine is not None else get_engine()
    SQLModel.metadata.create_all(eng)
    
    # 📌 
    with eng.begin() as connection:
        columnas = connection.execute(text("PRAGMA table_info(todos)")).mappings().all()
        nombres = {columna["name"] for columna in columnas}
        
        if "due_date" not in nombres:
            connection.execute(text("ALTER TABLE todos ADD COLUMN due_date TEXT"))
