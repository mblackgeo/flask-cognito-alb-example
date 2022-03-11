from datetime import datetime

import jwt

from webapp.auth.jwt_validator import JWTValidator


def make_jwt(header=None, claims=None) -> str:
    h = {
        "kid": "test",
    }
    if header:
        h.update(header)

    c = {
        "iss": "767676",
        "aud": "test",
        "exp": int(datetime.now().timestamp()) + 600,
    }
    if claims:
        c.update(claims)

    return jwt.encode(payload=c, headers=h, key="secret")


def test_jwt_validator_valid_key(mocker):
    mocker.patch(
        "webapp.auth.jwt_validator.JWTValidator.get_public_key", return_value="secret"
    )

    token = make_jwt()
    assert JWTValidator(token).is_valid()


def test_jwt_validator_wrong_aud(mocker):
    mocker.patch(
        "webapp.auth.jwt_validator.JWTValidator.get_public_key", return_value="secret"
    )

    token = make_jwt(claims={"aud": "wrong"})

    assert not JWTValidator(token).is_valid()


def test_jwt_validator_expired(mocker):
    mocker.patch(
        "webapp.auth.jwt_validator.JWTValidator.get_public_key", return_value="secret"
    )

    token = make_jwt(claims={"exp": int(datetime.now().timestamp()) - 600})

    assert not JWTValidator(token).is_valid()
