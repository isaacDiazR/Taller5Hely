"""
Configuración de fixtures compartidas para testing
"""
import pytest
from app import create_app
from app.models import task_repository


@pytest.fixture
def app():
    """Crea y configura una instancia de la app para testing"""
    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    """Cliente de testing para hacer requests a la API"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI runner para testing"""
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def reset_repository():
    """Limpia el repositorio antes de cada test"""
    task_repository.clear()
    yield
    task_repository.clear()


@pytest.fixture
def sample_task_data():
    """Datos de ejemplo para crear una tarea"""
    return {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 'high'
    }


@pytest.fixture
def multiple_tasks_data():
    """Múltiples tareas de ejemplo"""
    return [
        {'title': 'Task 1', 'description': 'First task', 'priority': 'high'},
        {'title': 'Task 2', 'description': 'Second task', 'priority': 'medium'},
        {'title': 'Task 3', 'description': 'Third task', 'priority': 'low'},
        {'title': 'Task 4', 'description': 'Fourth task', 'priority': 'high'},
        {'title': 'Task 5', 'description': 'Fifth task', 'priority': 'medium'}
    ]
