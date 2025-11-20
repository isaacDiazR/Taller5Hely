"""
Pruebas unitarias de validadores, modelos y utilidades
"""
from app.validators import validate_task_data
from app.models import Task, TaskRepository
from app.utils import (
    filter_tasks_by_status,
    filter_tasks_by_priority,
    search_tasks,
    sort_tasks_by_priority,
)


# ============================================
# TESTS DE VALIDACIÓN (15 pruebas)
# ============================================


class TestValidators:
    """Tests para validadores"""

    def test_valid_title(self):
        """Título válido debe pasar validación"""
        data = {"title": "Valid Task Title"}
        is_valid, message = validate_task_data(data)
        assert is_valid is True
        assert message == ""

    def test_empty_title(self):
        """Título vacío debe fallar"""
        data = {"title": ""}
        is_valid, message = validate_task_data(data)
        assert is_valid is False
        assert "empty" in message.lower()

    def test_missing_title(self):
        """Título faltante debe fallar"""
        data = {}
        is_valid, message = validate_task_data(data)
        assert is_valid is False
        assert "data" in message.lower() or "required" in message.lower()

    def test_title_too_long(self):
        """Título > 100 caracteres debe fallar"""
        data = {"title": "x" * 101}
        is_valid, message = validate_task_data(data)
        assert is_valid is False
        assert "100" in message

    def test_title_exactly_100_chars(self):
        """Título de exactamente 100 caracteres debe pasar"""
        data = {"title": "x" * 100}
        is_valid, message = validate_task_data(data)
        assert is_valid is True

    def test_valid_priority_low(self):
        """Prioridad 'low' válida"""
        data = {"title": "Task", "priority": "low"}
        is_valid, message = validate_task_data(data)
        assert is_valid is True

    def test_valid_priority_medium(self):
        """Prioridad 'medium' válida"""
        data = {"title": "Task", "priority": "medium"}
        is_valid, message = validate_task_data(data)
        assert is_valid is True

    def test_valid_priority_high(self):
        """Prioridad 'high' válida"""
        data = {"title": "Task", "priority": "high"}
        is_valid, message = validate_task_data(data)
        assert is_valid is True

    def test_invalid_priority(self):
        """Prioridad inválida debe fallar"""
        data = {"title": "Task", "priority": "urgent"}
        is_valid, message = validate_task_data(data)
        assert is_valid is False
        assert "priority" in message.lower()

    def test_valid_description(self):
        """Descripción válida debe pasar"""
        data = {"title": "Task", "description": "This is a description"}
        is_valid, message = validate_task_data(data)
        assert is_valid is True

    def test_description_too_long(self):
        """Descripción > 500 caracteres debe fallar"""
        data = {"title": "Task", "description": "x" * 501}
        is_valid, message = validate_task_data(data)
        assert is_valid is False
        assert "500" in message

    def test_description_exactly_500_chars(self):
        """Descripción de 500 caracteres debe pasar"""
        data = {"title": "Task", "description": "x" * 500}
        is_valid, message = validate_task_data(data)
        assert is_valid is True

    def test_completed_boolean_true(self):
        """Completed como boolean True debe pasar"""
        data = {"title": "Task", "completed": True}
        is_valid, message = validate_task_data(data)
        assert is_valid is True

    def test_completed_boolean_false(self):
        """Completed como boolean False debe pasar"""
        data = {"title": "Task", "completed": False}
        is_valid, message = validate_task_data(data)
        assert is_valid is True

    def test_completed_non_boolean(self):
        """Completed no-boolean debe fallar"""
        data = {"title": "Task", "completed": "true"}
        is_valid, message = validate_task_data(data)
        assert is_valid is False
        assert "boolean" in message.lower()


# ============================================
# TESTS DE MODELO TASK (20 pruebas)
# ============================================


class TestTaskModel:
    """Tests para el modelo Task"""

    def test_task_creation_minimal(self):
        """Crear tarea con datos mínimos"""
        task = Task(title="Test Task")
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False

    def test_task_creation_full(self):
        """Crear tarea con todos los datos"""
        task = Task(
            title="Test Task", description="Description", priority="high", task_id=1
        )
        assert task.title == "Test Task"
        assert task.description == "Description"
        assert task.priority == "high"
        assert task.id == 1

    def test_task_default_values(self):
        """Verificar valores por defecto"""
        task = Task(title="Task")
        assert task.completed is False
        assert task.priority == "medium"
        assert task.description == ""
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_timestamps(self):
        """Timestamps deben generarse automáticamente"""
        task = Task(title="Task")
        assert task.created_at is not None
        assert task.updated_at is not None
        assert "T" in task.created_at  # ISO format

    def test_task_to_dict(self):
        """Conversión a diccionario"""
        task = Task(title="Task", task_id=1)
        data = task.to_dict()
        assert isinstance(data, dict)
        assert data["id"] == 1
        assert data["title"] == "Task"
        assert "completed" in data
        assert "created_at" in data

    def test_task_update_title(self):
        """Actualizar título"""
        task = Task(title="Original")
        old_updated_at = task.updated_at
        task.update(title="Updated")
        assert task.title == "Updated"
        assert task.updated_at != old_updated_at

    def test_task_update_description(self):
        """Actualizar descripción"""
        task = Task(title="Task")
        task.update(description="New description")
        assert task.description == "New description"

    def test_task_update_priority(self):
        """Actualizar prioridad"""
        task = Task(title="Task")
        task.update(priority="high")
        assert task.priority == "high"

    def test_task_update_completed(self):
        """Actualizar estado completado"""
        task = Task(title="Task")
        assert task.completed is False
        task.update(completed=True)
        assert task.completed is True

    def test_task_update_multiple_fields(self):
        """Actualizar múltiples campos"""
        task = Task(title="Task")
        task.update(title="Updated", description="Desc", priority="low", completed=True)
        assert task.title == "Updated"
        assert task.description == "Desc"
        assert task.priority == "low"
        assert task.completed is True

    def test_task_id_not_updated(self):
        """ID no debe cambiar al actualizar"""
        task = Task(title="Task", task_id=1)
        task.update(id=999)
        assert task.id == 1

    def test_task_created_at_not_updated(self):
        """created_at no debe cambiar al actualizar"""
        task = Task(title="Task")
        original_created = task.created_at
        task.update(created_at="2025-01-01")
        assert task.created_at == original_created

    def test_task_priority_low(self):
        """Tarea con prioridad baja"""
        task = Task(title="Task", priority="low")
        assert task.priority == "low"

    def test_task_priority_medium(self):
        """Tarea con prioridad media"""
        task = Task(title="Task", priority="medium")
        assert task.priority == "medium"

    def test_task_priority_high(self):
        """Tarea con prioridad alta"""
        task = Task(title="Task", priority="high")
        assert task.priority == "high"

    def test_task_completion_toggle(self):
        """Alternar estado de completado"""
        task = Task(title="Task")
        assert task.completed is False
        task.update(completed=True)
        assert task.completed is True
        task.update(completed=False)
        assert task.completed is False

    def test_task_empty_description(self):
        """Descripción vacía por defecto"""
        task = Task(title="Task")
        assert task.description == ""

    def test_task_with_description(self):
        """Tarea con descripción"""
        task = Task(title="Task", description="Test description")
        assert task.description == "Test description"

    def test_task_dict_keys(self):
        """Verificar todas las claves en to_dict"""
        task = Task(title="Task", task_id=1)
        data = task.to_dict()
        expected_keys = [
            "id",
            "title",
            "description",
            "completed",
            "priority",
            "created_at",
            "updated_at",
        ]
        assert all(key in data for key in expected_keys)

    def test_task_update_updates_timestamp(self):
        """Update debe actualizar updated_at"""
        task = Task(title="Task")
        old_timestamp = task.updated_at
        import time

        time.sleep(0.01)
        task.update(title="New")
        assert task.updated_at != old_timestamp


# ============================================
# TESTS DE REPOSITORY (15 pruebas)
# ============================================


class TestTaskRepository:
    """Tests para TaskRepository"""

    def test_repository_create(self):
        """Crear tarea en repositorio"""
        repo = TaskRepository()
        task = Task(title="Task")
        created = repo.create(task)
        assert created.id == 1
        assert repo.count() == 1

    def test_repository_auto_increment_id(self):
        """IDs deben autoincrementarse"""
        repo = TaskRepository()
        task1 = repo.create(Task(title="Task 1"))
        task2 = repo.create(Task(title="Task 2"))
        assert task1.id == 1
        assert task2.id == 2

    def test_repository_get_existing(self):
        """Obtener tarea existente"""
        repo = TaskRepository()
        task = repo.create(Task(title="Task"))
        retrieved = repo.get(task.id)
        assert retrieved is not None
        assert retrieved.title == "Task"

    def test_repository_get_nonexistent(self):
        """Obtener tarea inexistente retorna None"""
        repo = TaskRepository()
        retrieved = repo.get(999)
        assert retrieved is None

    def test_repository_get_all(self):
        """Obtener todas las tareas"""
        repo = TaskRepository()
        repo.create(Task(title="Task 1"))
        repo.create(Task(title="Task 2"))
        all_tasks = repo.get_all()
        assert len(all_tasks) == 2

    def test_repository_get_all_empty(self):
        """Obtener todas cuando no hay tareas"""
        repo = TaskRepository()
        all_tasks = repo.get_all()
        assert len(all_tasks) == 0

    def test_repository_filter_by_completed(self):
        """Filtrar por estado completado"""
        repo = TaskRepository()
        task1 = repo.create(Task(title="Task 1"))
        repo.create(Task(title="Task 2"))
        repo.update(task1.id, completed=True)

        completed_tasks = repo.get_all(completed=True)
        assert len(completed_tasks) == 1
        assert completed_tasks[0].id == task1.id

    def test_repository_filter_by_priority(self):
        """Filtrar por prioridad"""
        repo = TaskRepository()
        repo.create(Task(title="Task 1", priority="high"))
        repo.create(Task(title="Task 2", priority="low"))

        high_priority = repo.get_all(priority="high")
        assert len(high_priority) == 1
        assert high_priority[0].priority == "high"

    def test_repository_update_existing(self):
        """Actualizar tarea existente"""
        repo = TaskRepository()
        task = repo.create(Task(title="Original"))
        updated = repo.update(task.id, title="Updated")
        assert updated.title == "Updated"

    def test_repository_update_nonexistent(self):
        """Actualizar tarea inexistente retorna None"""
        repo = TaskRepository()
        updated = repo.update(999, title="Updated")
        assert updated is None

    def test_repository_delete_existing(self):
        """Eliminar tarea existente"""
        repo = TaskRepository()
        task = repo.create(Task(title="Task"))
        success = repo.delete(task.id)
        assert success is True
        assert repo.count() == 0

    def test_repository_delete_nonexistent(self):
        """Eliminar tarea inexistente retorna False"""
        repo = TaskRepository()
        success = repo.delete(999)
        assert success is False

    def test_repository_count(self):
        """Contar total de tareas"""
        repo = TaskRepository()
        assert repo.count() == 0
        repo.create(Task(title="Task 1"))
        assert repo.count() == 1
        repo.create(Task(title="Task 2"))
        assert repo.count() == 2

    def test_repository_count_completed(self):
        """Contar tareas completadas"""
        repo = TaskRepository()
        task1 = repo.create(Task(title="Task 1"))
        repo.create(Task(title="Task 2"))
        repo.update(task1.id, completed=True)
        assert repo.count_completed() == 1

    def test_repository_count_by_priority(self):
        """Contar por prioridad"""
        repo = TaskRepository()
        repo.create(Task(title="T1", priority="high"))
        repo.create(Task(title="T2", priority="high"))
        repo.create(Task(title="T3", priority="low"))
        counts = repo.count_by_priority()
        assert counts["high"] == 2
        assert counts["medium"] == 0
        assert counts["low"] == 1


# ============================================
# TESTS DE UTILIDADES (10 pruebas)
# ============================================


class TestUtils:
    """Tests para funciones utilitarias"""

    def test_filter_by_status_completed(self):
        """Filtrar tareas completadas"""
        tasks = [Task(title="T1"), Task(title="T2")]
        tasks[0].completed = True

        filtered = filter_tasks_by_status(tasks, True)
        assert len(filtered) == 1
        assert filtered[0].title == "T1"

    def test_filter_by_status_pending(self):
        """Filtrar tareas pendientes"""
        tasks = [Task(title="T1"), Task(title="T2")]
        tasks[0].completed = True

        filtered = filter_tasks_by_status(tasks, False)
        assert len(filtered) == 1
        assert filtered[0].title == "T2"

    def test_filter_by_priority_high(self):
        """Filtrar por prioridad alta"""
        tasks = [Task(title="T1", priority="high"), Task(title="T2", priority="low")]

        filtered = filter_tasks_by_priority(tasks, "high")
        assert len(filtered) == 1
        assert filtered[0].priority == "high"

    def test_search_tasks_in_title(self):
        """Buscar en títulos"""
        tasks = [Task(title="Important Meeting"), Task(title="Buy groceries")]

        results = search_tasks(tasks, "meeting")
        assert len(results) == 1
        assert "Meeting" in results[0].title

    def test_search_tasks_in_description(self):
        """Buscar en descripciones"""
        tasks = [
            Task(title="Task 1", description="Python programming"),
            Task(title="Task 2", description="JavaScript coding"),
        ]

        results = search_tasks(tasks, "python")
        assert len(results) == 1

    def test_search_tasks_case_insensitive(self):
        """Búsqueda case-insensitive"""
        tasks = [Task(title="IMPORTANT TASK")]
        results = search_tasks(tasks, "important")
        assert len(results) == 1

    def test_search_tasks_no_results(self):
        """Búsqueda sin resultados"""
        tasks = [Task(title="Task")]
        results = search_tasks(tasks, "nonexistent")
        assert len(results) == 0

    def test_sort_by_priority_order(self):
        """Ordenar por prioridad: high, medium, low"""
        tasks = [
            Task(title="T1", priority="low"),
            Task(title="T2", priority="high"),
            Task(title="T3", priority="medium"),
        ]

        sorted_tasks = sort_tasks_by_priority(tasks)
        assert sorted_tasks[0].priority == "high"
        assert sorted_tasks[1].priority == "medium"
        assert sorted_tasks[2].priority == "low"

    def test_sort_preserves_order_within_priority(self):
        """Orden relativo dentro de misma prioridad"""
        tasks = [Task(title="T1", priority="high"), Task(title="T2", priority="high")]

        sorted_tasks = sort_tasks_by_priority(tasks)
        assert len(sorted_tasks) == 2
        assert all(t.priority == "high" for t in sorted_tasks)

    def test_filter_empty_list(self):
        """Filtrar lista vacía"""
        filtered = filter_tasks_by_status([], True)
        assert len(filtered) == 0
