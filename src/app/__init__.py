from flask import Flask

def create_app():
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)

    app.config['DEBUG'] = True

    from app.routes.api_routes import bp as api_bp
    app.register_blueprint(api_bp)

    return app