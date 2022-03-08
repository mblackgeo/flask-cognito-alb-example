"""Route declaration."""
from flask import Blueprint, Response, jsonify, render_template

bp = Blueprint("home_bp", __name__, template_folder="templates")


@bp.route("/")
def home() -> str:
    """Render the homepage of the website

    Parameters
    -------
    str
        HTML of page to display at "/"
    """
    return render_template(
        "index.html",
        title="Sample webapp",
        description="Testing Flask, AWS Cognito and an Application Load Balancer",
    )


@bp.route("/health")
def health() -> Response:
    """Return a 200 OK response. Used for automated health checks

    Returns
    -------
    flask.Response
        200 OK response
    """
    return jsonify({"status": "ok"})
