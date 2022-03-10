import logging
from datetime import datetime

from jwcrypto import jwt

from webapp.auth.jwt_validator import JWTValidator


def make_jwt(header=None, claims=None) -> jwt.JWT:
    h = {
        "alg": "RS256",
        "kid": "test",
    }
    if header:
        h.update(header)

    c = {
        "iss": "767676",
        "aud": "test",
        "iat": int(datetime.now().timestamp()),
        "exp": int(datetime.now().timestamp()) + 600,
    }
    if claims:
        c.update(claims)

    return jwt.JWT(header=h, claims=c)


def test_jwt_validator_valid_key(app, key):
    pub = key.export_public(as_dict=True)
    app.config["COGNITO_PUBLIC_KEYS"] = [pub]

    jwt_token = make_jwt()
    jwt_token.make_signed_token(key)
    signed_jwt = jwt_token.serialize()

    assert JWTValidator(signed_jwt).is_valid()


def test_jwt_validator_wrong_aud(app, key, caplog):
    pub = key.export_public(as_dict=True)
    app.config["COGNITO_PUBLIC_KEYS"] = [pub]

    jwt_token = make_jwt(claims={"aud": "wrong"})
    jwt_token.make_signed_token(key)
    signed_jwt = jwt_token.serialize()

    assert not JWTValidator(signed_jwt).is_valid()
    assert "Token was not issued for this audience" in caplog.text
