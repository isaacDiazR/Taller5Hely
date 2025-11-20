"""
Inicialización de la aplicación Flask
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os


def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)

    # Configuración de CORS para permitir requests desde el frontend
    CORS(app)

    # Configuración de la app
    app.config["JSON_SORT_KEYS"] = False
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

    # Registrar blueprints/routes
    from app.routes import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    # Obtener la ruta absoluta del directorio frontend
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

    # Servir archivos estáticos del frontend
    @app.route("/")
    def index():
        return send_from_directory(frontend_dir, "index.html")

    @app.route("/<path:path>")
    def static_files(path):
        # Evitar conflicto con rutas de API
        if path.startswith("api/"):
            return {"error": "Not found"}, 404
        return send_from_directory(frontend_dir, path)

    return app
