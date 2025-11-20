"""
Modelos de datos y lógica de negocio
"""

from datetime import datetime
from typing import Dict, List, Optional


class Task:
    """Modelo de Tarea"""

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        task_id: Optional[int] = None,
    ):
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = False
        self.priority = priority  # low, medium, high
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict:
        """Convierte la tarea a diccionario"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def update(self, **kwargs):
        """Actualiza los campos de la tarea"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ["id", "created_at"]:
                setattr(self, key, value)
        self.updated_at = datetime.utcnow().isoformat()


class TaskRepository:
    """Repositorio para gestión de tareas en memoria"""

    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1

    def create(self, task: Task) -> Task:
        """Crea una nueva tarea"""
        task.id = self.next_id
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Obtiene una tarea por ID"""
        return self.tasks.get(task_id)

    def get_all(
        self, completed: Optional[bool] = None, priority: Optional[str] = None
    ) -> List[Task]:
        """Obtiene todas las tareas con filtros opcionales"""
        tasks = list(self.tasks.values())

        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]

        if priority is not None:
            tasks = [t for t in tasks if t.priority == priority]

        return tasks

    def update(self, task_id: int, **kwargs) -> Optional[Task]:
        """Actualiza una tarea existente"""
        task = self.get(task_id)
        if task:
            task.update(**kwargs)
        return task

    def delete(self, task_id: int) -> bool:
        """Elimina una tarea"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def count(self) -> int:
        """Cuenta el total de tareas"""
        return len(self.tasks)

    def count_completed(self) -> int:
        """Cuenta tareas completadas"""
        return sum(1 for task in self.tasks.values() if task.completed)

    def count_by_priority(self) -> Dict[str, int]:
        """Cuenta tareas por prioridad"""
        counts = {"low": 0, "medium": 0, "high": 0}
        for task in self.tasks.values():
            if task.priority in counts:
                counts[task.priority] += 1
        return counts

    def clear(self):
        """Limpia todas las tareas (útil para testing)"""
        self.tasks.clear()
        self.next_id = 1


# Instancia global del repositorio
task_repository = TaskRepository()
