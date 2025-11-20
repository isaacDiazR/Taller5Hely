"""
Pruebas de rendimiento y performance
"""

import json
import time


class TestPerformance:
    """Tests de rendimiento de la API"""

    def test_perf_get_all_tasks_empty(self, client, benchmark):
        """Performance de GET /tasks sin datos"""

        def get_tasks():
            return client.get("/api/tasks")

        result = benchmark(get_tasks)
        assert result.status_code == 200
        # Benchmark automáticamente mide el tiempo

    def test_perf_get_all_tasks_with_data(self, client, benchmark):
        """Performance de GET /tasks con 100 tareas"""
        # Preparar: crear 100 tareas
        for i in range(100):
            client.post(
                "/api/tasks",
                data=json.dumps({"title": f"Task {i}"}),
                content_type="application/json",
            )

        def get_tasks():
            return client.get("/api/tasks")

        result = benchmark(get_tasks)
        assert result.status_code == 200
        data = json.loads(result.data)
        assert data["count"] == 100

    def test_perf_create_task(self, client, benchmark):
        """Performance de POST /tasks"""
        task_data = {
            "title": "Performance Test Task",
            "description": "Testing creation performance",
            "priority": "high",
        }

        def create_task():
            return client.post(
                "/api/tasks",
                data=json.dumps(task_data),
                content_type="application/json",
            )

        result = benchmark(create_task)
        assert result.status_code == 201

    def test_perf_update_task(self, client, benchmark):
        """Performance de PUT /tasks/<id>"""
        # Preparar: crear una tarea
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Original"}),
            content_type="application/json",
        )
        task_id = json.loads(response.data)["task"]["id"]

        update_data = {"title": "Updated", "completed": True}

        def update_task():
            return client.put(
                f"/api/tasks/{task_id}",
                data=json.dumps(update_data),
                content_type="application/json",
            )

        result = benchmark(update_task)
        assert result.status_code == 200

    def test_perf_delete_task(self, client, benchmark):
        """Performance de DELETE /tasks/<id>"""
        # Crear varias tareas para eliminar
        task_ids = []
        for i in range(10):
            response = client.post(
                "/api/tasks",
                data=json.dumps({"title": f"Task {i}"}),
                content_type="application/json",
            )
            task_ids.append(json.loads(response.data)["task"]["id"])

        current_id = [0]  # Usar lista para mutabilidad en closure

        def delete_task():
            task_id = task_ids[current_id[0] % len(task_ids)]
            current_id[0] += 1
            return client.delete(f"/api/tasks/{task_id}")

        result = benchmark(delete_task)
        # Nota: puede retornar 404 en ejecuciones posteriores
        assert result.status_code in [200, 404]

    def test_perf_get_task_by_id(self, client, benchmark):
        """Performance de GET /tasks/<id>"""
        # Preparar: crear tarea
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Task"}),
            content_type="application/json",
        )
        task_id = json.loads(response.data)["task"]["id"]

        def get_task():
            return client.get(f"/api/tasks/{task_id}")

        result = benchmark(get_task)
        assert result.status_code == 200

    def test_perf_filter_tasks(self, client, benchmark):
        """Performance de filtrado de tareas"""
        # Preparar: crear tareas con diferentes prioridades
        for i in range(50):
            priority = ["low", "medium", "high"][i % 3]
            client.post(
                "/api/tasks",
                data=json.dumps({"title": f"Task {i}", "priority": priority}),
                content_type="application/json",
            )

        def filter_tasks():
            return client.get("/api/tasks?priority=high&completed=false")

        result = benchmark(filter_tasks)
        assert result.status_code == 200

    def test_perf_get_stats(self, client, benchmark):
        """Performance de GET /stats"""
        # Preparar: crear tareas variadas
        for i in range(30):
            response = client.post(
                "/api/tasks",
                data=json.dumps(
                    {"title": f"Task {i}", "priority": ["low", "medium", "high"][i % 3]}
                ),
                content_type="application/json",
            )
            if i % 2 == 0:
                task_id = json.loads(response.data)["task"]["id"]
                client.put(
                    f"/api/tasks/{task_id}",
                    data=json.dumps({"completed": True}),
                    content_type="application/json",
                )

        def get_stats():
            return client.get("/api/stats")

        result = benchmark(get_stats)
        assert result.status_code == 200

    def test_perf_health_check(self, client, benchmark):
        """Performance de health check"""

        def health_check():
            return client.get("/api/health")

        result = benchmark(health_check)
        assert result.status_code == 200

    def test_perf_bulk_creation(self, client):
        """Performance de creación masiva de tareas"""
        start_time = time.time()

        # Crear 200 tareas
        for i in range(200):
            response = client.post(
                "/api/tasks",
                data=json.dumps({"title": f"Bulk Task {i}"}),
                content_type="application/json",
            )
            assert response.status_code == 201

        elapsed_time = time.time() - start_time

        # Verificar que se crearon todas
        response = client.get("/api/tasks")
        assert json.loads(response.data)["count"] == 200

        # Tiempo razonable para 200 creaciones (ajustar según necesidad)
        assert elapsed_time < 5.0  # Menos de 5 segundos

    def test_perf_sequential_updates(self, client):
        """Performance de actualizaciones secuenciales"""
        # Crear tarea
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "Task"}),
            content_type="application/json",
        )
        task_id = json.loads(response.data)["task"]["id"]

        start_time = time.time()

        # 100 actualizaciones consecutivas
        for i in range(100):
            response = client.put(
                f"/api/tasks/{task_id}",
                data=json.dumps({"description": f"Update {i}"}),
                content_type="application/json",
            )
            assert response.status_code == 200

        elapsed_time = time.time() - start_time

        # Tiempo razonable para 100 updates
        assert elapsed_time < 3.0  # Menos de 3 segundos

    def test_perf_mixed_operations(self, client):
        """Performance de operaciones mixtas"""
        start_time = time.time()

        operations = 0

        # 50 operaciones mixtas
        for i in range(50):
            # Crear
            response = client.post(
                "/api/tasks",
                data=json.dumps({"title": f"Task {i}"}),
                content_type="application/json",
            )
            task_id = json.loads(response.data)["task"]["id"]
            operations += 1

            # Leer
            client.get(f"/api/tasks/{task_id}")
            operations += 1

            # Actualizar
            client.put(
                f"/api/tasks/{task_id}",
                data=json.dumps({"completed": True}),
                content_type="application/json",
            )
            operations += 1

            # Leer stats cada 10 operaciones
            if i % 10 == 0:
                client.get("/api/stats")
                operations += 1

        elapsed_time = time.time() - start_time

        # 50 tareas × 3 ops + 5 stats = 155 operaciones
        ops_per_second = operations / elapsed_time

        # Al menos 30 operaciones por segundo
        assert ops_per_second > 30
