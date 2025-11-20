"""
Inicialización de la aplicación Flask
"""

from flask import Flask
from flask_cors import CORS


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

    return app
