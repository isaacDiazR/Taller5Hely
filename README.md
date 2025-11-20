# 📝 ToDo API - Taller de CI/CD y Testing

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![Tests](https://img.shields.io/badge/tests-112%20passing-success.svg)
![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

API REST completa de gestión de tareas con enfoque en **Integración Continua (CI/CD)** y **Testing Exhaustivo**. Proyecto desarrollado como parte del taller práctico de Ingeniería de Software.

## 🎯 Características Principales

- ✅ **API REST** completa con 7 endpoints CRUD
- ✅ **112 pruebas** automatizadas (unitarias, integración, E2E, performance)
- ✅ **96% de cobertura** de código
- ✅ **Pipeline CI/CD** con GitHub Actions
- ✅ **Containerización** con Docker
- ✅ **Frontend vanilla** (HTML/CSS/JS)
- ✅ **Documentación** completa

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.11**
- **Flask 3.0** - Framework web
- **Flask-CORS** - Soporte CORS para frontend
- **Almacenamiento en memoria** - Sin base de datos

### Testing
- **pytest 7.4.3** - Framework de pruebas
- **pytest-cov 4.1.0** - Cobertura de código
- **pytest-benchmark 4.0.0** - Pruebas de performance

### CI/CD
- **GitHub Actions** - Pipeline automatizado
- **Docker** - Contenedorización
- **flake8 & black** - Linting y formateo

### Frontend
- **HTML5 + CSS3 + JavaScript ES6**
- **Fetch API** - Consumo de API REST
- **Diseño responsive**

## 📁 Estructura del Proyecto

```
Taller5Hely/
├── app/                        # Código fuente de la API
│   ├── __init__.py            # Factory de la aplicación Flask
│   ├── routes.py              # Definición de endpoints
│   ├── models.py              # Modelos y repositorio
│   ├── validators.py          # Validaciones de entrada
│   └── utils.py               # Funciones auxiliares
│
├── tests/                      # Suite de pruebas
│   ├── conftest.py            # Fixtures compartidas
│   ├── test_unit.py           # 60 pruebas unitarias
│   ├── test_integration.py    # 30 pruebas de integración
│   ├── test_e2e.py            # 10 pruebas end-to-end
│   └── test_performance.py    # 12 pruebas de rendimiento
│
├── frontend/                   # Interfaz de usuario
│   ├── index.html             # Página principal
│   ├── css/style.css          # Estilos
│   └── js/app.js              # Lógica del frontend
│
├── .github/workflows/          # CI/CD
│   └── ci.yml                 # Pipeline de GitHub Actions
│
├── docs/                       # Documentación
│   ├── API_DOCUMENTATION.md   # Documentación de la API
│   └── TESTING_REPORT.md      # Reporte de pruebas
│
├── Dockerfile                  # Imagen Docker
├── docker-compose.yml          # Orquestación
├── requirements.txt            # Dependencias Python
├── pytest.ini                  # Configuración de pytest
├── .flake8                     # Configuración de linting
├── .gitignore                  # Archivos ignorados
├── run.py                      # Punto de entrada
├── PLAN_PROYECTO.md            # Plan detallado del proyecto
└── README.md                   # Este archivo
```

## 🚀 Instalación y Configuración

### Prerequisitos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Git
- Docker (opcional, para contenedores)

### Instalación Local

1. **Clonar el repositorio:**
```bash
git clone https://github.com/isaacDiazR/Taller5Hely.git
cd Taller5Hely
```

2. **Crear y activar entorno virtual:**
```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**
```bash
python run.py
```

La API estará disponible en: `http://localhost:5000`

### Instalación con Docker

1. **Construir imagen:**
```bash
docker build -t todo-api .
```

2. **Ejecutar contenedor:**
```bash
docker run -d -p 5000:5000 --name todo-api todo-api
```

### Usar Docker Compose

```bash
docker-compose up -d
```

## 📚 Uso de la API

### Endpoints Disponibles

#### Health Check
```http
GET /api/health
```

#### Listar Tareas
```http
GET /api/tasks
GET /api/tasks?completed=true
GET /api/tasks?priority=high
```

#### Obtener Tarea
```http
GET /api/tasks/{id}
```

#### Crear Tarea
```http
POST /api/tasks
Content-Type: application/json

{
  "title": "Mi tarea",
  "description": "Descripción opcional",
  "priority": "medium"
}
```

#### Actualizar Tarea
```http
PUT /api/tasks/{id}
Content-Type: application/json

{
  "title": "Título actualizado",
  "completed": true,
  "priority": "high"
}
```

#### Eliminar Tarea
```http
DELETE /api/tasks/{id}
```

#### Estadísticas
```http
GET /api/stats
```

**Ver documentación completa:** [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

## 🧪 Testing

### Ejecutar Todas las Pruebas

```bash
pytest
```

### Ejecutar con Cobertura

```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### Ejecutar por Tipo

```bash
# Pruebas unitarias
pytest tests/test_unit.py -v

# Pruebas de integración
pytest tests/test_integration.py -v

# Pruebas E2E
pytest tests/test_e2e.py -v

# Pruebas de rendimiento
pytest tests/test_performance.py -v
```

### Resultados

- **Total de pruebas:** 112
- **Pruebas pasando:** 112 (100%)
- **Cobertura de código:** 96.20%
- **Tiempo de ejecución:** ~6 segundos

**Desglose por tipo:**
- ✅ 60 pruebas unitarias
- ✅ 30 pruebas de integración
- ✅ 10 pruebas E2E
- ✅ 12 pruebas de performance

**Ver reporte completo:** [TESTING_REPORT.md](docs/TESTING_REPORT.md)

## 🔄 CI/CD Pipeline

El proyecto incluye un pipeline completo de CI/CD con GitHub Actions que se ejecuta en cada push y pull request:

### Etapas del Pipeline

1. **Lint and Format**
   - Verificación con flake8
   - Validación de formato con black

2. **Tests**
   - Ejecución en Python 3.9, 3.10 y 3.11
   - Pruebas unitarias, integración, E2E y performance

3. **Coverage**
   - Generación de reporte de cobertura
   - Validación mínima del 80%
   - Upload a Codecov (opcional)

4. **Docker Build**
   - Construcción de imagen Docker
   - Test del contenedor
   - Verificación de health check

5. **Security Scan**
   - Análisis con safety
   - Escaneo con bandit

### Configuración

El pipeline se encuentra en `.github/workflows/ci.yml`

## 🐳 Docker

### Dockerfile

Imagen optimizada con multi-stage build:
- Imagen base: `python:3.11-slim`
- Health check integrado
- Usuario no-root para seguridad

### docker-compose.yml

Orquestación simple con:
- Servicio API en puerto 5000
- Health checks configurados
- Restart automático

### Comandos Útiles

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart
```

## 🌐 Frontend

El proyecto incluye una interfaz web completa en `frontend/`:

### Características del Frontend

- ✅ Crear, editar y eliminar tareas
- ✅ Marcar tareas como completadas
- ✅ Filtrar por estado y prioridad
- ✅ Ver estadísticas en tiempo real
- ✅ Diseño responsive (mobile-first)
- ✅ Sin frameworks (vanilla JS)

### Uso

1. Iniciar el backend:
```bash
python run.py
```

2. Abrir `frontend/index.html` en el navegador

**Nota:** Requiere que la API esté corriendo en `http://localhost:5000`

## 📊 Métricas del Proyecto

### Cobertura de Código

| Módulo | Statements | Missing | Cover |
|--------|-----------|---------|-------|
| app/__init__.py | 10 | 0 | 100% |
| app/models.py | 60 | 0 | 100% |
| app/routes.py | 67 | 1 | 99% |
| app/utils.py | 12 | 0 | 100% |
| app/validators.py | 35 | 6 | 83% |
| **TOTAL** | **184** | **7** | **96.20%** |

### Performance

| Endpoint | Tiempo Promedio |
|----------|----------------|
| GET /api/health | ~127 µs |
| GET /api/tasks | ~152 µs |
| POST /api/tasks | ~191 µs |
| PUT /api/tasks/{id} | ~198 µs |
| DELETE /api/tasks/{id} | ~156 µs |
| GET /api/stats | ~159 µs |

## 🏗️ Buenas Prácticas Implementadas

### Código
- ✅ Principios SOLID
- ✅ Separation of Concerns
- ✅ Repository Pattern
- ✅ Factory Pattern
- ✅ Validaciones exhaustivas

### Testing
- ✅ AAA Pattern (Arrange-Act-Assert)
- ✅ Test fixtures y reutilización
- ✅ Coverage > 80%
- ✅ Tests aislados e independientes

### DevOps
- ✅ CI/CD automatizado
- ✅ Docker para consistencia
- ✅ Linting y formateo automático
- ✅ Security scans

## 🤝 Contribución

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución

- Seguir PEP 8 para código Python
- Mantener cobertura de tests > 80%
- Documentar nuevos endpoints
- Actualizar CHANGELOG

## 📝 Próximas Mejoras

- [ ] Autenticación JWT
- [ ] Base de datos PostgreSQL
- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Despliegue en Heroku/Railway
- [ ] Tests de carga con Locust
- [ ] Monitoreo con Prometheus

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autor

**Isaac Díaz**
- GitHub: [@isaacDiazR](https://github.com/isaacDiazR)
- Proyecto: Taller de Integración Continua y Testing
- Universidad: UNAM FES Cuautitlán
- Materia: Ingeniería de Software

## 🙏 Agradecimientos

- Profesor y equipo docente de Ingeniería de Software
- Comunidad de Flask y pytest
- Documentación de GitHub Actions y Docker

---

**Fecha de creación:** Noviembre 2025  
**Última actualización:** Noviembre 2025  
**Versión:** 1.0.0

⭐ Si te ha sido útil este proyecto, considera darle una estrella en GitHub
