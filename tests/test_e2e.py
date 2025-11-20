"""
Pruebas End-to-End simulando usuarios reales
"""

import json


# Nota: Estas pruebas requieren que el servidor esté corriendo
# Para testing, usaremos el test client de Flask
class TestE2ETaskLifecycle:
    """Tests E2E del ciclo de vida completo de tareas"""

    def test_e2e_complete_task_lifecycle(self, client):
        """Ciclo completo: crear -> leer -> actualizar -> eliminar"""
        # 1. Crear tarea
        create_response = client.post(
            "/api/tasks",
            data=json.dumps(
                {
                    "title": "E2E Test Task",
                    "description": "Testing complete lifecycle",
                    "priority": "high",
                }
            ),
            content_type="application/json",
        )
        assert create_response.status_code == 201
        task = json.loads(create_response.data)["task"]
        task_id = task["id"]

        # 2. Leer tarea creada
        read_response = client.get(f"/api/tasks/{task_id}")
        assert read_response.status_code == 200
        task_data = json.loads(read_response.data)["task"]
        assert task_data["title"] == "E2E Test Task"
        assert task_data["completed"] is False

        # 3. Actualizar tarea
        update_response = client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"title": "Updated E2E Task", "completed": True}),
            content_type="application/json",
        )
        assert update_response.status_code == 200

        # 4. Verificar actualización
        verify_response = client.get(f"/api/tasks/{task_id}")
        updated_task = json.loads(verify_response.data)["task"]
        assert updated_task["title"] == "Updated E2E Task"
        assert updated_task["completed"] is True

        # 5. Eliminar tarea
        delete_response = client.delete(f"/api/tasks/{task_id}")
        assert delete_response.status_code == 200

        # 6. Verificar eliminación
        final_response = client.get(f"/api/tasks/{task_id}")
        assert final_response.status_code == 404

    def test_e2e_multiple_users_scenario(self, client):
        """Simular múltiples usuarios creando tareas"""
        users_tasks = {
            "user1": [
                {"title": "User 1 - Task 1", "priority": "high"},
                {"title": "User 1 - Task 2", "priority": "medium"},
            ],
            "user2": [
                {"title": "User 2 - Task 1", "priority": "low"},
                {"title": "User 2 - Task 2", "priority": "high"},
            ],
        }

        # Crear tareas para cada usuario
        for user, tasks in users_tasks.items():
            for task in tasks:
                response = client.post(
                    "/api/tasks", data=json.dumps(task), content_type="application/json"
                )
                assert response.status_code == 201

        # Verificar que todas las tareas se crearon
        all_tasks_response = client.get("/api/tasks")
        all_tasks = json.loads(all_tasks_response.data)
        assert all_tasks["count"] == 4

    def test_e2e_data_persistence_in_memory(self, client):
        """Verificar persistencia de datos en memoria durante sesión"""
        # Crear múltiples tareas
        task_ids = []
        for i in range(5):
            response = client.post(
                "/api/tasks",
                data=json.dumps({"title": f"Persistent Task {i}"}),
                content_type="application/json",
            )
            task_ids.append(json.loads(response.data)["task"]["id"])

        # Realizar operaciones en cada tarea
        for task_id in task_ids:
            # Actualizar
            client.put(
                f"/api/tasks/{task_id}",
                data=json.dumps({"description": f"Updated desc {task_id}"}),
                content_type="application/json",
            )

        # Verificar que todas persisten con cambios
        for task_id in task_ids:
            response = client.get(f"/api/tasks/{task_id}")
            task = json.loads(response.data)["task"]
            assert task["description"] == f"Updated desc {task_id}"

    def test_e2e_error_recovery(self, client):
        """Recuperación ante errores y continuidad del servicio"""
        # 1. Operación exitosa
        success_response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Good Task"}),
            content_type="application/json",
        )
        assert success_response.status_code == 201

        # 2. Operación fallida (datos inválidos)
        fail_response = client.post(
            "/api/tasks",
            data=json.dumps({"title": ""}),
            content_type="application/json",
        )
        assert fail_response.status_code == 400

        # 3. Otra operación exitosa después del error
        recovery_response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Recovery Task"}),
            content_type="application/json",
        )
        assert recovery_response.status_code == 201

        # 4. Verificar que ambas tareas exitosas están
        all_tasks = client.get("/api/tasks")
        assert json.loads(all_tasks.data)["count"] == 2

    def test_e2e_filtering_workflow(self, client):
        """Flujo completo de filtrado de tareas"""
        # Crear tareas con diferentes estados y prioridades
        tasks_config = [
            {"title": "High Priority Done", "priority": "high", "complete": True},
            {"title": "High Priority Pending", "priority": "high", "complete": False},
            {"title": "Low Priority Done", "priority": "low", "complete": True},
            {"title": "Low Priority Pending", "priority": "low", "complete": False},
            {
                "title": "Medium Priority Pending",
                "priority": "medium",
                "complete": False,
            },
        ]

        # Crear y configurar tareas
        for config in tasks_config:
            response = client.post(
                "/api/tasks",
                data=json.dumps(
                    {"title": config["title"], "priority": config["priority"]}
                ),
                content_type="application/json",
            )
            task_id = json.loads(response.data)["task"]["id"]

            if config["complete"]:
                client.put(
                    f"/api/tasks/{task_id}",
                    data=json.dumps({"completed": True}),
                    content_type="application/json",
                )

        # Testear filtros
        # Filtro: solo completadas
        completed = client.get("/api/tasks?completed=true")
        assert json.loads(completed.data)["count"] == 2

        # Filtro: solo pendientes
        pending = client.get("/api/tasks?completed=false")
        assert json.loads(pending.data)["count"] == 3

        # Filtro: alta prioridad
        high_priority = client.get("/api/tasks?priority=high")
        assert json.loads(high_priority.data)["count"] == 2

    def test_e2e_stats_tracking(self, client):
        """Seguimiento de estadísticas en tiempo real"""
        # Estado inicial
        initial_stats = client.get("/api/stats")
        assert json.loads(initial_stats.data)["total"] == 0

        # Crear 3 tareas de alta prioridad
        for i in range(3):
            client.post(
                "/api/tasks",
                data=json.dumps({"title": f"High {i}", "priority": "high"}),
                content_type="application/json",
            )

        # Verificar stats
        stats1 = client.get("/api/stats")
        data1 = json.loads(stats1.data)
        assert data1["total"] == 3
        assert data1["by_priority"]["high"] == 3
        assert data1["pending"] == 3

        # Completar 2 tareas
        client.put(
            "/api/tasks/1",
            data=json.dumps({"completed": True}),
            content_type="application/json",
        )
        client.put(
            "/api/tasks/2",
            data=json.dumps({"completed": True}),
            content_type="application/json",
        )

        # Verificar stats actualizadas
        stats2 = client.get("/api/stats")
        data2 = json.loads(stats2.data)
        assert data2["completed"] == 2
        assert data2["pending"] == 1

    def test_e2e_health_monitoring(self, client):
        """Monitoreo de salud del servicio durante operaciones"""
        # Health check inicial
        health1 = client.get("/api/health")
        assert json.loads(health1.data)["status"] == "healthy"

        # Realizar operaciones intensivas
        for i in range(20):
            client.post(
                "/api/tasks",
                data=json.dumps({"title": f"Task {i}"}),
                content_type="application/json",
            )

        # Health check después de carga
        health2 = client.get("/api/health")
        assert json.loads(health2.data)["status"] == "healthy"

        # Operaciones de actualización
        for i in range(1, 21):
            client.put(
                f"/api/tasks/{i}",
                data=json.dumps({"completed": True}),
                content_type="application/json",
            )

        # Health check final
        health3 = client.get("/api/health")
        assert json.loads(health3.data)["status"] == "healthy"

    def test_e2e_sequential_operations(self, client):
        """Operaciones secuenciales complejas"""
        task_id = None

        # 1. Crear tarea inicial
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Sequential Task", "priority": "low"}),
            content_type="application/json",
        )
        task_id = json.loads(response.data)["task"]["id"]

        # 2. Actualizar prioridad a media
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"priority": "medium"}),
            content_type="application/json",
        )

        # 3. Agregar descripción
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"description": "Added description"}),
            content_type="application/json",
        )

        # 4. Actualizar título
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"title": "Updated Sequential Task"}),
            content_type="application/json",
        )

        # 5. Completar tarea
        client.put(
            f"/api/tasks/{task_id}",
            data=json.dumps({"completed": True}),
            content_type="application/json",
        )

        # 6. Verificar estado final
        final = client.get(f"/api/tasks/{task_id}")
        task = json.loads(final.data)["task"]
        assert task["title"] == "Updated Sequential Task"
        assert task["description"] == "Added description"
        assert task["priority"] == "medium"
        assert task["completed"] is True

    def test_e2e_validation_boundaries(self, client):
        """Probar límites de validación"""
        # Título en el límite (100 caracteres)
        title_100 = "a" * 100
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": title_100}),
            content_type="application/json",
        )
        assert response.status_code == 201

        # Título sobre el límite (101 caracteres)
        title_101 = "a" * 101
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": title_101}),
            content_type="application/json",
        )
        assert response.status_code == 400

        # Descripción en el límite (500 caracteres)
        desc_500 = "b" * 500
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Task", "description": desc_500}),
            content_type="application/json",
        )
        assert response.status_code == 201

    def test_e2e_api_consistency(self, client):
        """Verificar consistencia de la API a través de operaciones"""
        # Crear 5 tareas
        for i in range(5):
            client.post(
                "/api/tasks",
                data=json.dumps({"title": f"Task {i}"}),
                content_type="application/json",
            )

        # Verificar conteo en diferentes endpoints
        all_tasks = client.get("/api/tasks")
        stats = client.get("/api/stats")

        all_count = json.loads(all_tasks.data)["count"]
        stats_total = json.loads(stats.data)["total"]

        assert all_count == stats_total == 5

        # Eliminar 2 tareas
        client.delete("/api/tasks/1")
        client.delete("/api/tasks/2")

        # Verificar consistencia después de eliminación
        all_tasks2 = client.get("/api/tasks")
        stats2 = client.get("/api/stats")

        all_count2 = json.loads(all_tasks2.data)["count"]
        stats_total2 = json.loads(stats2.data)["total"]

        assert all_count2 == stats_total2 == 3
