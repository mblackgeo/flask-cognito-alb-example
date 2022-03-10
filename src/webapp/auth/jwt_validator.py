"""
Utilis for verifying JSON Web Tokens
See also:
https://github.com/awslabs/aws-support-tools/tree/master/Cognito/decode-verify-jwt
"""
import base64
import json
import logging
from typing import Dict, Optional

import requests
from flask import current_app as app
from jwcrypto import jwk, jwt
from jwcrypto.common import JWException


class JWTValidator:
    def __init__(self, token: str):
        self.token: str = token
        self.client_id: str = app.config["COGNITO_APP_CLIENT_ID"]

        logging.warning(f"JWT:\n{self.token}")

    def get_key_id(self) -> str:
        """Extract the key ID from the JWT headers"""
        jwt_headers = self.token.split(".")[0]
        decoded_jwt_headers = base64.b64decode(jwt_headers).decode("utf-8")
        decoded_json = json.loads(decoded_jwt_headers)
        return decoded_json["kid"]

    def get_public_key(self, kid: str) -> jwk.JWK:
        # The ALB signs the JWT with a dynamic key
        region = app.config["AWS_REGION"]
        url = f"https://public-keys.auth.elb.{region}.amazonaws.com/{kid}"
        req = requests.get(url)
        return jwk.JWK.from_pem(bytes(req.text, encoding="utf-8"))

    def decode_and_verify(
        self, key: jwk.JWK, check_claims: Optional[Dict[str, str]] = None
    ) -> jwt.JWT:
        """Decode and verify a JWT with a given JWK

        Parameters
        ----------
        key : jwk.JWK
            They JSON Web Key used to verify the token
        check_claims : Optional[Dict[str, str]], optional
            Additional claims to check, by default None.
            If not set, it will check expiry. If set it will check the passed
            values instead.

        Returns
        -------
        jwt.JWT
            The decoded token
        """
        return jwt.JWT(
            jwt=self.token,
            key=key,
            check_claims=check_claims,
        )

    def is_valid(self) -> bool:
        """Return True if the JWT is signed by the ALB public key"""
        # get the key ID from the headers prior to verification
        kid = self.get_key_id()

        # Grab the actual public key from the ALB endpoint
        key = self.get_public_key(kid)
        if key is None:
            logging.warning("No matching public key not found to verify signature")
            return False

        # Decode and verify the JWT, this will verify expiry as well
        try:
            token = self.decode_and_verify(key=key)
        except JWException as e:
            logging.warning(e)
            return False

        # now check any additional claims are correct
        try:
            token = self.decode_and_verify(
                key=key,
                check_claims={"aud": app.config["COGNITO_APP_CLIENT_ID"]},
            )
        except JWException as e:
            logging.warning(e)
            return False

        logging.warning(f"Validated JWT : {token}")

        return True
