"""Persistencia y CRUD sobre una base temporal: nunca usan data/todos.db."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import patch
from sqlalchemy import text
from sqlmodel import create_engine
from todo_app.models import Todo
from todo_app.repository import TodoRepository
from todo_app.todo_app import TodoState


class CrudTests(TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.url = f'sqlite:///{Path(self.directory.name)/"test.db"}'
        self.engine = create_engine(self.url,connect_args={'check_same_thread':False})
        self.repo = TodoRepository(self.engine)
        self.repo.initialize()

    def tearDown(self):
        self.engine.dispose()
        self.directory.cleanup()

    def test_full_crud_survives_new_connection(self):
        first = self.repo.create('  Grabar vídeo  ','  Preparar ejemplo  ')
        self.assertEqual(first.title,'Grabar vídeo')
        self.assertEqual(first.description,'Preparar ejemplo')
        self.repo.edit(first.id,'Grabar clase','')
        self.repo.set_completed(first.id,True)
        second_engine = create_engine(self.url)
        try:
            reopened = TodoRepository(second_engine).list_all()
            self.assertEqual(len(reopened),1)
            self.assertTrue(reopened[0].completed)
            self.assertEqual(reopened[0].created_at,first.created_at)
            self.assertEqual(reopened[0].title,'Grabar clase')
            self.assertEqual(reopened[0].description,'')
        finally:
            second_engine.dispose()
        self.repo.delete(first.id)
        self.assertEqual(self.repo.list_all(),[])
        next_task = self.repo.create('Otra tarea')
        self.assertGreater(next_task.id,first.id)

    def test_invalid_text_and_missing_id(self):
        for title,description in [('   ',''),('x'*161,''),('válido','x'*3001)]:
            with self.assertRaises(ValueError):self.repo.create(title,description)
        for action in [lambda:self.repo.edit(100,'válida'),lambda:self.repo.set_completed(100,True),lambda:self.repo.delete(100)]:
            with self.assertRaises(ValueError):action()
        self.assertEqual(self.repo.list_all(),[])

    def test_new_timestamp_per_instance(self):
        a,b=Todo(title='A'),Todo(title='B')
        self.assertIsNot(a.created_at,b.created_at)
        self.assertIsNotNone(a.created_at.tzinfo)

    def test_due_date_hours_and_progress_survive_reconnection(self):
        task = self.repo.create('Entrega', estimated_hours='2,5', due_date='2026-11-20')
        self.repo.set_progress(task.id, 40)
        self.repo.edit(task.id, 'Entrega revisada')
        engine = create_engine(self.url)
        try:
            saved = TodoRepository(engine).list_all()[0]
            self.assertEqual(saved.due_date, '2026-11-20')
            self.assertEqual(saved.estimated_hours, 2.5)
            self.assertEqual(saved.progress, 40)
        finally:
            engine.dispose()
        self.assertEqual(self.repo.create('Sin fecha').due_date, '')
        for value in ['2026-02-30', '20/11/2026', '20261120']:
            with self.assertRaises(ValueError):
                self.repo.create('Inválida', due_date=value)
        for value in ['-1', 'nan', 'inf', 'abc']:
            with self.assertRaises(ValueError):
                self.repo.create('Inválida', estimated_hours=value, due_date='2026-11-20')

    def test_due_date_migration_preserves_existing_data(self):
        engine = create_engine(f'sqlite:///{Path(self.directory.name)/"legacy.db"}')
        try:
            with engine.begin() as connection:
                connection.execute(text(
                    'CREATE TABLE todos (id INTEGER PRIMARY KEY AUTOINCREMENT, '
                    'title TEXT NOT NULL, description TEXT, completed BOOLEAN NOT NULL, '
                    'created_at DATETIME NOT NULL, estimated_hours REAL NOT NULL DEFAULT 0, '
                    'progress INTEGER NOT NULL DEFAULT 0)'
                ))
                connection.execute(text(
                    "INSERT INTO todos (title, completed, created_at, estimated_hours, progress) "
                    "VALUES ('Existente', 0, '2026-11-09 12:00:00', 3.5, 60)"
                ))
            repo = TodoRepository(engine)
            repo.initialize()
            repo.initialize()
            task = repo.list_all()[0]
            self.assertEqual(task.title, 'Existente')
            self.assertEqual(task.estimated_hours, 3.5)
            self.assertEqual(task.progress, 60)
            self.assertEqual(task.due_date, '')
        finally:
            engine.dispose()

    def test_state_saves_date_and_preserves_input_on_error(self):
        state = TodoState(_reflex_internal_init=True)
        with patch('todo_app.todo_app.TodoRepository', lambda: self.repo):
            state.load_todos()
            state.set_new_title('Entrega')
            state.set_new_estimated_hours('2.5')
            state.set_new_due_date('2026-02-30')
            state.add_todo()
            self.assertTrue(state.error)
            self.assertEqual(state.new_due_date, '2026-02-30')
            self.assertEqual(self.repo.list_all(), [])
            state.set_new_due_date('2026-11-20')
            state.add_todo()
            self.assertFalse(state.error)
            self.assertEqual(state.todos[0].due_date, '2026-11-20')
            self.assertEqual(state.todos[0].estimated_hours, 2.5)
            self.assertEqual(state.new_due_date, '')
            self.assertEqual(state.new_estimated_hours, '')

    def test_state_validation_edit_filters_and_database(self):
        s = TodoState(_reflex_internal_init=True)
        with patch('todo_app.todo_app.TodoRepository',lambda:self.repo):
            s.load_todos()
            s.set_new_title(' ');s.add_todo()
            self.assertTrue(s.error)
            s.set_new_title('Aprender Reflex');s.set_new_description('Practicar SQL');s.add_todo()
            self.assertFalse(s.error)
            self.assertEqual(s.new_title,'')
            task=s.todos[0]
            s.toggle_complete(task.id,True)
            self.assertEqual(s.completed_count,1)
            s.set_filter('Pendientes');self.assertEqual(s.visible_todos,[])
            s.set_filter('Todas');s.set_search('sql');self.assertEqual(len(s.visible_todos),1)
            s.start_edit(task.id);s.set_edit_title(' ');s.update_todo()
            self.assertTrue(s.edit_open);self.assertTrue(s.edit_error)
            s.set_edit_title('Reflex CRUD');s.update_todo()
            self.assertFalse(s.edit_open)
            self.assertEqual(s.todos[0].title,'Reflex CRUD')
            other = TodoState(_reflex_internal_init=True);other.load_todos()
            self.assertEqual(other.todos[0].title,'Reflex CRUD')
            s.ask_delete(task.id);s.delete_todo()
            self.assertEqual(self.repo.list_all(),[])


if __name__=='__main__':main()
