"""Route declaration."""
from flask import Response
from flask import current_app as app
from flask import jsonify, render_template


@app.route("/")
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


@app.route("/health")
def health() -> Response:
    """Return a 200 OK response. Used for automated health checks

    Returns
    -------
    flask.Response
        200 OK response
    """
    return jsonify({"status": "ok"})
