import logging
import os

import pytest

from webapp import create_app


@pytest.fixture
def app():
    """Create application for the tests."""
    # setup testing config
    os.environ["FLASK_APP"] = "webapp"
    os.environ["FLASK_ENV"] = "test"
    os.environ["SECRET_KEY"] = "not-used"

    _app = create_app()
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    _app.config["TESTING"] = True
    _app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False

    _app.testing = True

    yield _app
    ctx.pop()


@pytest.fixture
def client(app):
    cl = app.test_client()
    yield cl
