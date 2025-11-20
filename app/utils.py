"""
Funciones auxiliares
"""

from typing import List
from app.models import Task


def filter_tasks_by_status(tasks: List[Task], completed: bool) -> List[Task]:
    """Filtra tareas por estado de completado"""
    return [task for task in tasks if task.completed == completed]


def filter_tasks_by_priority(tasks: List[Task], priority: str) -> List[Task]:
    """Filtra tareas por prioridad"""
    return [task for task in tasks if task.priority == priority]


def search_tasks(tasks: List[Task], query: str) -> List[Task]:
    """Busca tareas por texto en título o descripción"""
    query_lower = query.lower()
    return [
        task
        for task in tasks
        if query_lower in task.title.lower() or query_lower in task.description.lower()
    ]


def sort_tasks_by_priority(tasks: List[Task]) -> List[Task]:
    """Ordena tareas por prioridad (high -> medium -> low)"""
    priority_order = {"high": 0, "medium": 1, "low": 2}
    return sorted(tasks, key=lambda t: priority_order.get(t.priority, 3))
