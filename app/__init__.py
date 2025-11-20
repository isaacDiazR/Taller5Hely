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

    # Servir archivos estáticos del frontend
    @app.route("/")
    def index():
        return send_from_directory("frontend", "index.html")

    @app.route("/<path:path>")
    def static_files(path):
        return send_from_directory("frontend", path)

    return app
