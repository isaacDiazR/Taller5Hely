"""
Rutas de la API REST
"""
from flask import Blueprint, request, jsonify
from app.models import Task, task_repository
from app.validators import validate_task_data
from datetime import datetime

api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check del servicio"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'ToDo API'
    }), 200


@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Obtiene todas las tareas con filtros opcionales"""
    # Obtener parámetros de query
    completed_param = request.args.get('completed')
    priority_param = request.args.get('priority')
    
    # Convertir parámetro completed a boolean
    completed = None
    if completed_param is not None:
        completed = completed_param.lower() == 'true'
    
    # Obtener tareas con filtros
    tasks = task_repository.get_all(completed=completed, priority=priority_param)
    
    return jsonify({
        'tasks': [task.to_dict() for task in tasks],
        'count': len(tasks)
    }), 200


@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Obtiene una tarea específica por ID"""
    task = task_repository.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({'task': task.to_dict()}), 200


@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """Crea una nueva tarea"""
    data = request.get_json()
    
    # Validar datos
    is_valid, error_message = validate_task_data(data)
    if not is_valid:
        return jsonify({'error': error_message}), 400
    
    # Crear tarea
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium')
    )
    
    created_task = task_repository.create(task)
    
    return jsonify({
        'task': created_task.to_dict(),
        'message': 'Task created successfully'
    }), 201


@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Actualiza una tarea existente"""
    task = task_repository.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    # Validar solo si hay datos a actualizar
    if data:
        # Preparar datos para validación (solo los campos presentes)
        validation_data = {}
        if 'title' in data:
            validation_data['title'] = data['title']
        if 'priority' in data:
            validation_data['priority'] = data['priority']
        if 'description' in data:
            validation_data['description'] = data['description']
        if 'completed' in data:
            validation_data['completed'] = data['completed']
        
        # Si no hay título en la actualización, usar el existente para validación
        if 'title' not in validation_data:
            validation_data['title'] = task.title
        
        is_valid, error_message = validate_task_data(validation_data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
    
    # Actualizar tarea
    updated_task = task_repository.update(task_id, **data)
    
    return jsonify({
        'task': updated_task.to_dict(),
        'message': 'Task updated successfully'
    }), 200


@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Elimina una tarea"""
    success = task_repository.delete(task_id)
    
    if not success:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({'message': 'Task deleted successfully'}), 200


@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Obtiene estadísticas de las tareas"""
    total = task_repository.count()
    completed = task_repository.count_completed()
    by_priority = task_repository.count_by_priority()
    
    return jsonify({
        'total': total,
        'completed': completed,
        'pending': total - completed,
        'by_priority': by_priority
    }), 200
