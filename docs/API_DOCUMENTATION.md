# 📚 Documentación de la API - ToDo API

## Base URL

```
http://localhost:5000/api
```

---

## Endpoints

### 1. Health Check

Verifica que el servicio esté activo y funcionando correctamente.

#### Request
```http
GET /api/health
```

#### Response
```json
{
  "status": "healthy",
  "timestamp": "2025-11-19T10:30:00.123456",
  "service": "ToDo API"
}
```

#### Status Codes
- `200 OK` - Servicio funcionando correctamente

---

### 2. Listar Tareas

Obtiene todas las tareas con filtros opcionales.

#### Request
```http
GET /api/tasks
GET /api/tasks?completed=true
GET /api/tasks?priority=high
GET /api/tasks?completed=false&priority=medium
```

#### Query Parameters

| Parámetro | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `completed` | boolean | Filtrar por estado | `true`, `false` |
| `priority` | string | Filtrar por prioridad | `low`, `medium`, `high` |

#### Response
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Completar informe",
      "description": "Informe mensual de ventas",
      "completed": false,
      "priority": "high",
      "created_at": "2025-11-19T10:00:00.123456",
      "updated_at": "2025-11-19T10:00:00.123456"
    }
  ],
  "count": 1
}
```

#### Status Codes
- `200 OK` - Tareas obtenidas exitosamente

---

### 3. Obtener Tarea por ID

Obtiene una tarea específica por su ID.

#### Request
```http
GET /api/tasks/{id}
```

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id` | integer | ID de la tarea |

#### Response - Éxito
```json
{
  "task": {
    "id": 1,
    "title": "Completar informe",
    "description": "Informe mensual de ventas",
    "completed": false,
    "priority": "high",
    "created_at": "2025-11-19T10:00:00.123456",
    "updated_at": "2025-11-19T10:00:00.123456"
  }
}
```

#### Response - Error
```json
{
  "error": "Task not found"
}
```

#### Status Codes
- `200 OK` - Tarea encontrada
- `404 Not Found` - Tarea no existe

---

### 4. Crear Tarea

Crea una nueva tarea.

#### Request
```http
POST /api/tasks
Content-Type: application/json

{
  "title": "Nueva tarea",
  "description": "Descripción opcional",
  "priority": "medium"
}
```

#### Request Body

| Campo | Tipo | Requerido | Descripción | Validación |
|-------|------|-----------|-------------|------------|
| `title` | string | ✅ Sí | Título de la tarea | Max 100 caracteres |
| `description` | string | ❌ No | Descripción detallada | Max 500 caracteres |
| `priority` | string | ❌ No | Prioridad | `low`, `medium`, `high` (default: `medium`) |

#### Response - Éxito
```json
{
  "task": {
    "id": 1,
    "title": "Nueva tarea",
    "description": "Descripción opcional",
    "completed": false,
    "priority": "medium",
    "created_at": "2025-11-19T10:00:00.123456",
    "updated_at": "2025-11-19T10:00:00.123456"
  },
  "message": "Task created successfully"
}
```

#### Response - Error
```json
{
  "error": "Title is required"
}
```

#### Status Codes
- `201 Created` - Tarea creada exitosamente
- `400 Bad Request` - Datos inválidos

---

### 5. Actualizar Tarea

Actualiza una tarea existente.

#### Request
```http
PUT /api/tasks/{id}
Content-Type: application/json

{
  "title": "Título actualizado",
  "description": "Nueva descripción",
  "priority": "high",
  "completed": true
}
```

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id` | integer | ID de la tarea |

#### Request Body

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `title` | string | ❌ No | Nuevo título |
| `description` | string | ❌ No | Nueva descripción |
| `priority` | string | ❌ No | Nueva prioridad |
| `completed` | boolean | ❌ No | Estado de completado |

**Nota:** Solo se actualizan los campos enviados en el request.

#### Response - Éxito
```json
{
  "task": {
    "id": 1,
    "title": "Título actualizado",
    "description": "Nueva descripción",
    "completed": true,
    "priority": "high",
    "created_at": "2025-11-19T10:00:00.123456",
    "updated_at": "2025-11-19T10:05:00.123456"
  },
  "message": "Task updated successfully"
}
```

#### Response - Error
```json
{
  "error": "Task not found"
}
```

#### Status Codes
- `200 OK` - Tarea actualizada exitosamente
- `400 Bad Request` - Datos inválidos
- `404 Not Found` - Tarea no existe

---

### 6. Eliminar Tarea

Elimina una tarea existente.

#### Request
```http
DELETE /api/tasks/{id}
```

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id` | integer | ID de la tarea |

#### Response - Éxito
```json
{
  "message": "Task deleted successfully"
}
```

#### Response - Error
```json
{
  "error": "Task not found"
}
```

#### Status Codes
- `200 OK` - Tarea eliminada exitosamente
- `404 Not Found` - Tarea no existe

---

### 7. Estadísticas

Obtiene estadísticas generales de las tareas.

#### Request
```http
GET /api/stats
```

#### Response
```json
{
  "total": 10,
  "completed": 4,
  "pending": 6,
  "by_priority": {
    "low": 2,
    "medium": 5,
    "high": 3
  }
}
```

#### Status Codes
- `200 OK` - Estadísticas obtenidas exitosamente

---

## Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| `200 OK` | Solicitud exitosa |
| `201 Created` | Recurso creado exitosamente |
| `400 Bad Request` | Datos de entrada inválidos |
| `404 Not Found` | Recurso no encontrado |
| `500 Internal Server Error` | Error interno del servidor |

---

## Validaciones

### Título (title)
- ✅ **Requerido:** Sí
- ✅ **Tipo:** String
- ✅ **Min:** 1 carácter (sin espacios)
- ✅ **Max:** 100 caracteres
- ❌ **No puede estar vacío**

### Descripción (description)
- ✅ **Requerido:** No
- ✅ **Tipo:** String
- ✅ **Max:** 500 caracteres
- ✅ **Default:** String vacío

### Prioridad (priority)
- ✅ **Requerido:** No
- ✅ **Tipo:** String (enum)
- ✅ **Valores:** `low`, `medium`, `high`
- ✅ **Default:** `medium`

### Completado (completed)
- ✅ **Requerido:** No
- ✅ **Tipo:** Boolean
- ✅ **Default:** `false`

---

## Ejemplos de Uso

### Crear tarea con curl

```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Revisar código",
    "description": "Code review del PR #42",
    "priority": "high"
  }'
```

### Obtener todas las tareas pendientes de alta prioridad

```bash
curl "http://localhost:5000/api/tasks?completed=false&priority=high"
```

### Marcar tarea como completada

```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### Eliminar tarea

```bash
curl -X DELETE http://localhost:5000/api/tasks/1
```

---

## Modelos de Datos

### Task (Tarea)

```json
{
  "id": 1,                                    // integer - ID único autogenerado
  "title": "Completar informe",               // string - Título de la tarea
  "description": "Informe mensual",           // string - Descripción opcional
  "completed": false,                         // boolean - Estado de completado
  "priority": "high",                         // string - Prioridad (low/medium/high)
  "created_at": "2025-11-19T10:00:00.123456", // string (ISO 8601) - Fecha de creación
  "updated_at": "2025-11-19T10:00:00.123456"  // string (ISO 8601) - Última actualización
}
```

### Stats (Estadísticas)

```json
{
  "total": 10,           // integer - Total de tareas
  "completed": 4,        // integer - Tareas completadas
  "pending": 6,          // integer - Tareas pendientes
  "by_priority": {       // object - Conteo por prioridad
    "low": 2,
    "medium": 5,
    "high": 3
  }
}
```

---

## Manejo de Errores

### Formato de Error

Todos los errores siguen este formato:

```json
{
  "error": "Descripción del error"
}
```

### Errores Comunes

#### Título vacío
```json
{
  "error": "Title cannot be empty"
}
```

#### Título muy largo
```json
{
  "error": "Title cannot exceed 100 characters"
}
```

#### Prioridad inválida
```json
{
  "error": "Priority must be one of: low, medium, high"
}
```

#### Tarea no encontrada
```json
{
  "error": "Task not found"
}
```

---

## Notas Importantes

1. **Almacenamiento:** Los datos se almacenan en memoria y se pierden al reiniciar el servidor
2. **CORS:** Habilitado para permitir requests desde cualquier origen
3. **IDs:** Los IDs son autoincrementales y no se reutilizan
4. **Timestamps:** Todas las fechas están en formato ISO 8601 UTC
5. **Actualización parcial:** PUT permite actualizar solo los campos enviados

---

## Limitaciones Actuales

- ❌ Sin autenticación/autorización
- ❌ Sin paginación para grandes listas
- ❌ Sin búsqueda por texto
- ❌ Sin ordenamiento personalizado
- ❌ Sin persistencia en base de datos

---

**Versión de la API:** 1.0  
**Última actualización:** Noviembre 2025
