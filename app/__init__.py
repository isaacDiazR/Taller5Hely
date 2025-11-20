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

    # Obtener la ruta absoluta del directorio frontend
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

    # Servir archivos estáticos del frontend ANTES del blueprint de API
    @app.route("/")
    def index():
        return send_from_directory(frontend_dir, "index.html")

    @app.route("/css/<path:path>")
    def serve_css(path):
        return send_from_directory(os.path.join(frontend_dir, "css"), path)

    @app.route("/js/<path:path>")
    def serve_js(path):
        return send_from_directory(os.path.join(frontend_dir, "js"), path)

    # Registrar blueprints/routes
    from app.routes import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    return app
