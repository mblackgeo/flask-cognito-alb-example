"""
Helper functions for verifying JSON Web Tokens
"""
import logging
from typing import List

import jwt
import requests
from flask import current_app as app


class JWTValidator:
    def __init__(self, token: str):
        self.token: str = token

    def get_public_key(self, kid: str) -> str:
        """Retrive the public key PEM from the Elastic Load Balancer"""
        # The ALB signs the JWT with a dynamic key
        region = app.config["AWS_REGION"]
        url = f"https://public-keys.auth.elb.{region}.amazonaws.com/{kid}"
        req = requests.get(url)
        return req.text

    @property
    def allowed_algorithms(self) -> List[str]:
        if app.config["TESTING"]:
            return ["HS256"]

        return ["ES256"]

    def is_valid(self) -> bool:
        """Return True if the JWT is signed by the ALB public key"""
        # get the key ID from the headers prior to verification
        kid = jwt.get_unverified_header(self.token)["kid"]

        # Grab the public key from the ALB endpoint
        pub_key = self.get_public_key(kid)

        # TODO set to debug
        logging.warning(f"Encoded token: {self.token}")
        logging.warning(f"KID: {kid}")

        # decode and verify the JWT
        try:
            jwt.decode(
                jwt=self.token,
                key=pub_key,
                algorithms=self.allowed_algorithms,
                options={
                    "verify_signature": True,
                    "verify_aud": False,
                    "verify_iss": False,
                    "verify_exp": True,
                    "verify_iat": True,
                    "verify_nbf": False,
                },
            )
        except jwt.PyJWTError as err:
            logging.warning(f"Failed to verify token:\n{err}".format(err))
            return False
        return True
