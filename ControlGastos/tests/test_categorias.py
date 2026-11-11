"""Pruebas de categorías con una base SQLite temporal."""

from contextlib import contextmanager

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker

from gestion_gastos import seed, services
from gestion_gastos.database import Base
from gestion_gastos.models import Category
from gestion_gastos.schemas import CategoryRead
from gestion_gastos.state import AppState


@pytest.fixture
def factory(monkeypatch, tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'prueba.db'}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    @contextmanager
    def fake_session():
        with session_factory() as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise

    monkeypatch.setattr(seed, "get_session", fake_session)
    monkeypatch.setattr(services, "get_session", fake_session)
    return session_factory


def count(factory) -> int:
    with factory() as session:
        return session.scalar(select(func.count()).select_from(Category))


def test_seed_no_duplica(factory):
    seed.seed_categories()
    seed.seed_categories()
    assert count(factory) == len(seed.DEFAULT_CATEGORIES)


def test_seed_respeta_categorias_existentes(factory):
    with factory() as session:
        session.add(Category(id=42, name="Ocio"))
        session.commit()
    seed.seed_categories()
    with factory() as session:
        ocio = session.scalars(select(Category).where(Category.name == "Ocio")).all()
    assert [(c.id, c.name) for c in ocio] == [(42, "Ocio")]
    assert count(factory) == len(seed.DEFAULT_CATEGORIES)


def test_list_categories_devuelve_category_read_en_orden(factory):
    seed.seed_categories()
    result = services.list_categories()
    assert all(isinstance(item, CategoryRead) for item in result)
    assert [item.name for item in result] == list(seed.DEFAULT_CATEGORIES)


def test_estado_carga_y_conserva_el_id(factory):
    seed.seed_categories()
    state = AppState(_reflex_internal_init=True)
    AppState.load_categories.fn(state)
    assert len(state.categories) == len(seed.DEFAULT_CATEGORIES)
    assert state.category_id is None and state.category_pending

    AppState.set_selected_category.fn(state, "3")
    assert state.category_id == 3 and not state.category_pending

    AppState.set_selected_category.fn(state, "999")  # ID inexistente: se ignora
    assert state.category_id == 3

    AppState.select_category_for_edit.fn(state, 5)  # precarga al editar
    assert state.category_id == 5


def test_estado_avisa_si_no_hay_tablas(monkeypatch):
    def fallo():
        raise RuntimeError("sin tablas")

    monkeypatch.setattr("gestion_gastos.state.list_categories", fallo)
    state = AppState(_reflex_internal_init=True)
    AppState.load_categories.fn(state)
    assert state.categories == [] and "migración" in state.category_error
