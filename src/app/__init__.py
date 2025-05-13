from flask import Flask

def create_app():
    """Create and configure the Flask application.
    Returns:
        Flask: The Flask application instance.
    """
    app = Flask(__name__)

    app.config['DEBUG'] = True

    from app.routes.routes import bp as api_bp
    app.register_blueprint(api_bp)

    return app