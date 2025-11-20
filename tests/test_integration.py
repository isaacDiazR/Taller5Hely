"""
Pruebas de integración de endpoints y flujos completos
"""

import json


# ============================================
# TESTS DE ENDPOINTS BÁSICOS (12 pruebas)
# ============================================


class TestHealthEndpoint:
    """Tests del endpoint de health"""

    def test_health_check_success(self, client):
        """Health check debe retornar 200"""
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_check_content(self, client):
        """Health check debe retornar contenido correcto"""
        response = client.get("/api/health")
        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "service" in data


class TestCreateTaskEndpoint:
    """Tests del endpoint POST /tasks"""

    def test_create_task_success(self, client, sample_task_data):
        """Crear tarea con datos válidos"""
        response = client.post(
            "/api/tasks",
            data=json.dumps(sample_task_data),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert "task" in data
        assert data["task"]["title"] == sample_task_data["title"]

    def test_create_task_missing_title(self, client):
        """Crear tarea sin título debe fallar"""
        response = client.post(
            "/api/tasks",
            data=json.dumps({"description": "No title"}),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_create_task_empty_title(self, client):
        """Crear tarea con título vacío debe fallar"""
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": ""}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_create_task_invalid_priority(self, client):
        """Crear tarea con prioridad inválida debe fallar"""
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Task", "priority": "invalid"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_create_task_assigns_id(self, client, sample_task_data):
        """Crear tarea debe asignar ID automáticamente"""
        response = client.post(
            "/api/tasks",
            data=json.dumps(sample_task_data),
            content_type="application/json",
        )
        data = json.loads(response.data)
        assert data["task"]["id"] is not None
        assert isinstance(data["task"]["id"], int)

    def test_create_task_default_completed_false(self, client):
        """Nueva tarea debe tener completed=False por defecto"""
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Task"}),
            content_type="application/json",
        )
        data = json.loads(response.data)
        assert data["task"]["completed"] is False


class TestGetTasksEndpoint:
    """Tests del endpoint GET /tasks"""

    def test_get_all_tasks_empty(self, client):
        """Obtener tareas cuando no hay ninguna"""
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["count"] == 0
        assert len(data["tasks"]) == 0

    def test_get_all_tasks(self, client, multiple_tasks_data):
        """Obtener todas las tareas"""
        # Crear varias tareas
        for task_data in multiple_tasks_data:
            client.post(
                "/api/tasks",
                data=json.dumps(task_data),
                content_type="application/json",
            )

        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["count"] == len(multiple_tasks_data)
        assert len(data["tasks"]) == len(multiple_tasks_data)

    def test_get_tasks_filter_completed(self, client):
        """Filtrar tareas completadas"""
        # Crear tarea y completarla
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Task 1"}),
            content_type="application/json",
        )
        task_id = json.loads(response.data)["task"]["id"]
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"completed": True}),
            content_type="application/json",
        )

        # Crear otra tarea sin completar
        client.post(
            "/api/tasks",
            data=json.dumps({"title": "Task 2"}),
            content_type="application/json",
        )

        # Filtrar completadas
        response = client.get("/api/tasks?completed=true")
        data = json.loads(response.data)
        assert data["count"] == 1
        assert data["tasks"][0]["completed"] is True

    def test_get_tasks_filter_pending(self, client):
        """Filtrar tareas pendientes"""
        # Crear tarea completada
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Task 1"}),
            content_type="application/json",
        )
        task_id = json.loads(response.data)["task"]["id"]
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"completed": True}),
            content_type="application/json",
        )

        # Crear tarea pendiente
        client.post(
            "/api/tasks",
            data=json.dumps({"title": "Task 2"}),
            content_type="application/json",
        )

        # Filtrar pendientes
        response = client.get("/api/tasks?completed=false")
        data = json.loads(response.data)
        assert data["count"] == 1
        assert data["tasks"][0]["completed"] is False

    def test_get_tasks_filter_by_priority(self, client):
        """Filtrar tareas por prioridad"""
        client.post(
            "/api/tasks",
            data=json.dumps({"title": "T1", "priority": "high"}),
            content_type="application/json",
        )
        client.post(
            "/api/tasks",
            data=json.dumps({"title": "T2", "priority": "low"}),
            content_type="application/json",
        )

        response = client.get("/api/tasks?priority=high")
        data = json.loads(response.data)
        assert data["count"] == 1
        assert data["tasks"][0]["priority"] == "high"


class TestGetTaskByIdEndpoint:
    """Tests del endpoint GET /tasks/<id>"""

    def test_get_task_by_id_success(self, client, sample_task_data):
        """Obtener tarea existente por ID"""
        # Crear tarea
        create_response = client.post(
            "/api/tasks",
            data=json.dumps(sample_task_data),
            content_type="application/json",
        )
        task_id = json.loads(create_response.data)["task"]["id"]

        # Obtener por ID
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["task"]["id"] == task_id

    def test_get_task_nonexistent(self, client):
        """Obtener tarea inexistente debe retornar 404"""
        response = client.get("/api/tasks/999")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data


class TestUpdateTaskEndpoint:
    """Tests del endpoint PUT /tasks/<id>"""

    def test_update_task_success(self, client, sample_task_data):
        """Actualizar tarea existente"""
        # Crear tarea
        create_response = client.post(
            "/api/tasks",
            data=json.dumps(sample_task_data),
            content_type="application/json",
        )
        task_id = json.loads(create_response.data)["task"]["id"]

        # Actualizar
        update_data = {"title": "Updated Task"}
        response = client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["task"]["title"] == "Updated Task"

    def test_update_task_nonexistent(self, client):
        """Actualizar tarea inexistente debe retornar 404"""
        response = client.put(
            "/api/tasks/999",
            data=json.dumps({"title": "Updated"}),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_update_task_mark_completed(self, client):
        """Marcar tarea como completada"""
        # Crear tarea
        create_response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Task"}),
            content_type="application/json",
        )
        task_id = json.loads(create_response.data)["task"]["id"]

        # Completar
        response = client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"completed": True}),
            content_type="application/json",
        )
        data = json.loads(response.data)
        assert data["task"]["completed"] is True


class TestDeleteTaskEndpoint:
    """Tests del endpoint DELETE /tasks/<id>"""

    def test_delete_task_success(self, client, sample_task_data):
        """Eliminar tarea existente"""
        # Crear tarea
        create_response = client.post(
            "/api/tasks",
            data=json.dumps(sample_task_data),
            content_type="application/json",
        )
        task_id = json.loads(create_response.data)["task"]["id"]

        # Eliminar
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 200

        # Verificar que ya no existe
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_nonexistent(self, client):
        """Eliminar tarea inexistente debe retornar 404"""
        response = client.delete("/api/tasks/999")
        assert response.status_code == 404


class TestStatsEndpoint:
    """Tests del endpoint GET /stats"""

    def test_stats_empty(self, client):
        """Estadísticas sin tareas"""
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["total"] == 0
        assert data["completed"] == 0
        assert data["pending"] == 0

    def test_stats_with_tasks(self, client):
        """Estadísticas con tareas"""
        # Crear tareas
        response1 = client.post(
            "/api/tasks",
            data=json.dumps({"title": "T1", "priority": "high"}),
            content_type="application/json",
        )
        task_id = json.loads(response1.data)["task"]["id"]
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"completed": True}),
            content_type="application/json",
        )

        client.post(
            "/api/tasks",
            data=json.dumps({"title": "T2", "priority": "low"}),
            content_type="application/json",
        )

        # Obtener stats
        response = client.get("/api/stats")
        data = json.loads(response.data)
        assert data["total"] == 2
        assert data["completed"] == 1
        assert data["pending"] == 1
        assert data["by_priority"]["high"] == 1
        assert data["by_priority"]["low"] == 1


# ============================================
# TESTS DE FLUJOS COMPLETOS (8 pruebas)
# ============================================


class TestUserFlows:
    """Tests de flujos completos de usuario"""

    def test_create_and_complete_task_flow(self, client):
        """Flujo: Crear tarea y marcarla como completada"""
        # Crear
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "My Task"}),
            content_type="application/json",
        )
        assert response.status_code == 201
        task_id = json.loads(response.data)["task"]["id"]

        # Completar
        response = client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"completed": True}),
            content_type="application/json",
        )
        assert response.status_code == 200

        # Verificar
        response = client.get(f"/api/tasks/{task_id}")
        data = json.loads(response.data)
        assert data["task"]["completed"] is True

    def test_create_update_delete_flow(self, client):
        """Flujo completo: Crear -> Actualizar -> Eliminar"""
        # Crear
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Original"}),
            content_type="application/json",
        )
        task_id = json.loads(response.data)["task"]["id"]

        # Actualizar
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"title": "Updated"}),
            content_type="application/json",
        )

        # Verificar actualización
        response = client.get(f"/api/tasks/{task_id}")
        assert json.loads(response.data)["task"]["title"] == "Updated"

        # Eliminar
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 200

        # Verificar eliminación
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 404

    def test_multiple_tasks_management(self, client, multiple_tasks_data):
        """Gestión de múltiples tareas"""
        task_ids = []

        # Crear múltiples tareas
        for task_data in multiple_tasks_data:
            response = client.post(
                "/api/tasks",
                data=json.dumps(task_data),
                content_type="application/json",
            )
            task_ids.append(json.loads(response.data)["task"]["id"])

        # Verificar que todas se crearon
        response = client.get("/api/tasks")
        assert json.loads(response.data)["count"] == len(multiple_tasks_data)

        # Completar algunas
        for i in range(0, len(task_ids), 2):
            client.put(
                f"/api/tasks/{task_ids[i]}",
                data=json.dumps({"completed": True}),
                content_type="application/json",
            )

        # Verificar filtrado
        response = client.get("/api/tasks?completed=true")
        assert json.loads(response.data)["count"] == 3

    def test_priority_workflow(self, client):
        """Flujo de trabajo con prioridades"""
        # Crear tareas con diferentes prioridades
        priorities = ["low", "medium", "high"]
        for priority in priorities:
            client.post(
                "/api/tasks",
                data=json.dumps({"title": f"Task {priority}", "priority": priority}),
                content_type="application/json",
            )

        # Verificar filtrado por cada prioridad
        for priority in priorities:
            response = client.get(f"/api/tasks?priority={priority}")
            data = json.loads(response.data)
            assert data["count"] == 1
            assert data["tasks"][0]["priority"] == priority

    def test_bulk_operations(self, client):
        """Operaciones en lote"""
        # Crear 10 tareas
        task_ids = []
        for i in range(10):
            response = client.post(
                "/api/tasks",
                data=json.dumps({"title": f"Task {i}"}),
                content_type="application/json",
            )
            task_ids.append(json.loads(response.data)["task"]["id"])

        # Completar todas
        for task_id in task_ids:
            client.put(
                f"/api/tasks/{task_id}",
                data=json.dumps({"completed": True}),
                content_type="application/json",
            )

        # Verificar estadísticas
        response = client.get("/api/stats")
        data = json.loads(response.data)
        assert data["total"] == 10
        assert data["completed"] == 10
        assert data["pending"] == 0

    def test_update_priority_flow(self, client):
        """Flujo de actualización de prioridad"""
        # Crear tarea con prioridad baja
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Task", "priority": "low"}),
            content_type="application/json",
        )
        task_id = json.loads(response.data)["task"]["id"]

        # Escalar a media
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"priority": "medium"}),
            content_type="application/json",
        )
        response = client.get(f"/api/tasks/{task_id}")
        assert json.loads(response.data)["task"]["priority"] == "medium"

        # Escalar a alta
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"priority": "high"}),
            content_type="application/json",
        )
        response = client.get(f"/api/tasks/{task_id}")
        assert json.loads(response.data)["task"]["priority"] == "high"

    def test_error_recovery_flow(self, client):
        """Flujo de recuperación de errores"""
        # Intentar crear tarea inválida
        response = client.post(
            "/api/tasks", data=json.dumps({}), content_type="application/json"
        )
        assert response.status_code == 400

        # Crear tarea válida después del error
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Valid Task"}),
            content_type="application/json",
        )
        assert response.status_code == 201

        # Verificar que la tarea válida se creó
        response = client.get("/api/tasks")
        assert json.loads(response.data)["count"] == 1

    def test_concurrent_operations(self, client):
        """Operaciones concurrentes simuladas"""
        # Crear tarea
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Shared Task"}),
            content_type="application/json",
        )
        task_id = json.loads(response.data)["task"]["id"]

        # Múltiples actualizaciones consecutivas
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"description": "Update 1"}),
            content_type="application/json",
        )
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"description": "Update 2"}),
            content_type="application/json",
        )
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"description": "Final Update"}),
            content_type="application/json",
        )

        # Verificar última actualización
        response = client.get(f"/api/tasks/{task_id}")
        data = json.loads(response.data)
        assert data["task"]["description"] == "Final Update"
