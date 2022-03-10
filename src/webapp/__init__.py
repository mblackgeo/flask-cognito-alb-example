import json
import urllib

from flask import Flask

__version__ = "0.1.0"
__all__ = ["__version__", "create_app"]


def create_app() -> Flask:
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object("webapp.config.WebappConfig")

    if app.config.get("COGNITO_USERPOOL_ID") is not None:
        # Populate the Cognito public keys
        region = app.config.get("AWS_REGION")
        userpool_id = app.config.get("COGNITO_USERPOOL_ID")
        keys_url = (
            f"https://cognito-idp.{region}.amazonaws.com/"
            f"{userpool_id}/.well-known/jwks.json"
        )

        with urllib.request.urlopen(keys_url) as f:
            response = f.read()

        app.config["COGNITO_PUBLIC_KEYS"] = json.loads(response.decode("utf-8"))["keys"]

    with app.app_context():
        from .auth import routes as auth_routes  # noqa: F401
        from .home import routes as home_routes  # noqa: F401

        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(home_routes.bp)

        return app
