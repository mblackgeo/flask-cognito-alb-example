from flask import Flask

__version__ = "0.1.0"
__all__ = ["__version__", "create_app"]


def create_app() -> Flask:
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object("webapp.config.WebappConfig")

    with app.app_context():
        from .auth import routes as auth_routes  # noqa: F401
        from .home import routes as home_routes  # noqa: F401

        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(home_routes.bp)

        return app
