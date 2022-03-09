"""Route declaration."""
import requests
from flask import Blueprint, Response
from flask import current_app as app
from flask import jsonify, make_response, redirect, request, url_for

bp = Blueprint("auth_bp", __name__)


@bp.route("/user")
def user() -> Response:
    """
    Calls the Cognito User Info endpoint
    """

    url = app.config.get("USER_INFO_URL")
    if url:
        access_token = request.headers.get("x-amzn-oidc-accesstoken")
        response = requests.get(
            url, headers={"Authorization": f"Bearer {access_token}"}
        )
        return response.json()

    return jsonify({"status": "Cognito not in use"})


@bp.route("/logout")
def logout() -> Response:
    """
    This handles the logout action for the app if Cognito is used, else
    redirects to the homepage
    """
    logout_url = app.config.get("LOGOUT_URL")

    if logout_url:
        # Looks a little weird, but this is the only way to get an HTTPS redirect
        response = make_response(
            redirect(app.config.get("LOGOUT_URL", f"https://{request.host}/"))
        )

        # Invalidate the session cookie
        response.set_cookie("AWSELBAuthSessionCookie-0", "empty", max_age=-3600)

        return response

    return redirect(url_for("home_bp.home"))
