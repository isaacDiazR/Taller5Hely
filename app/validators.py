"""
Validadores de datos de entrada
"""
from typing import Dict, Tuple


class ValidationError(Exception):
    """Excepción personalizada para errores de validación"""

    pass


def validate_task_data(data: Dict) -> Tuple[bool, str]:
    """
    Valida los datos de una tarea

    Returns:
        Tuple[bool, str]: (es_válido, mensaje_error)
    """
    if not data:
        return False, "No data provided"

    # Validar título
    if "title" not in data:
        return False, "Title is required"

    title = data.get("title", "").strip()
    if not title:
        return False, "Title cannot be empty"

    if len(title) > 100:
        return False, "Title cannot exceed 100 characters"

    # Validar prioridad si está presente
    if "priority" in data:
        priority = data.get("priority")
        valid_priorities = ["low", "medium", "high"]
        if priority not in valid_priorities:
            return False, f"Priority must be one of: {', '.join(valid_priorities)}"

    # Validar descripción si está presente
    if "description" in data:
        description = data.get("description", "")
        if len(description) > 500:
            return False, "Description cannot exceed 500 characters"

    # Validar completed si está presente
    if "completed" in data:
        completed = data.get("completed")
        if not isinstance(completed, bool):
            return False, "Completed must be a boolean value"

    return True, ""


def validate_priority(priority: str) -> bool:
    """Valida que la prioridad sea válida"""
    return priority in ["low", "medium", "high"]


def validate_title(title: str) -> Tuple[bool, str]:
    """Valida el título de una tarea"""
    if not title or not title.strip():
        return False, "Title cannot be empty"

    if len(title) > 100:
        return False, "Title cannot exceed 100 characters"

    return True, ""
