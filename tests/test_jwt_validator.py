from datetime import datetime

import jwt

from webapp.auth.jwt_validator import JWTValidator


def make_jwt(expiry_time=None) -> str:
    if expiry_time is None:
        expiry_time = int(datetime.now().timestamp()) + 600

    return jwt.encode(
        payload={
            "exp": expiry_time,
        },
        headers={
            "kid": "test",
        },
        key="secret",
        algorithm="HS256",
    )


def test_jwt_validator_valid_key(mocker):
    mocker.patch(
        "webapp.auth.jwt_validator.JWTValidator.get_public_key", return_value="secret"
    )

    token = make_jwt()
    assert JWTValidator(token).is_valid()


def test_jwt_validator_expired(mocker):
    mocker.patch(
        "webapp.auth.jwt_validator.JWTValidator.get_public_key", return_value="secret"
    )

    token = make_jwt(expiry_time=int(datetime.now().timestamp()) - 600)
    assert not JWTValidator(token).is_valid()
