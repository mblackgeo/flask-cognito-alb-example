"""
Utilis for verifying JSON Web Tokens
See also:
https://github.com/awslabs/aws-support-tools/tree/master/Cognito/decode-verify-jwt
"""
import logging
import time
from typing import Dict, List, Optional

from flask import current_app as app
from jose import jwk, jwt
from jose.utils import base64url_decode


class JWTValidator:
    def __init__(self, token: str):
        self.token: str = token
        self.keys: List[Dict[str, str]] = app.config["COGNITO_PUBLIC_KEYS"]
        self.client_id: str = app.config["COGNITO_APP_CLIENT_ID"]

    def _get_public_key(self, kid: str) -> Optional[Dict[str, str]]:
        for key in self.keys:
            if key["kid"] == kid:
                return key
        return None

    def is_valid(self) -> bool:
        """Return True if the JWT is signed by the Cognito public keys"""
        # get the public key ID from the headers prior to verification
        headers = jwt.get_unverified_headers(self.token)
        pkey = self._get_public_key(headers["kid"])
        if pkey is None:
            logging.warning("No matching public key not found to verify signature")
            return False

        # construct the public key
        public_key = jwk.construct(pkey)

        # get the last two sections of the token
        # message and signature (encoded in base64)
        message, encoded_signature = str(self.token).rsplit(".", 1)

        # decode and verify the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            logging.warning("Signature verification failed")
            return False

        # since we passed the verification, can safely use the unverified claims
        claims = jwt.get_unverified_claims(self.token)

        # verify the token is not expired
        if time.time() > claims["exp"]:
            logging.warning("Token has expired")
            return False

        # check the audience is correct
        if claims["aud"] != self.client_id:
            logging.warning("Token was not issued for this audience")
            return False

        return True
