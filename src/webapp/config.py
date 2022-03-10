"""App configuration."""
from os import urandom
from os.path import abspath, dirname, join
from typing import Dict, List, Optional

from pydantic import BaseSettings, Field


class WebappConfig(BaseSettings):
    SECRET_KEY: Optional[str] = Field(default=str(urandom(32)))
    FLASK_APP: Optional[str] = Field(default="webapp")
    FLASK_ENV: Optional[str] = Field(default="dev")
    TEMPLATES_FOLDER = "templates"

    AWS_REGION: Optional[str] = Field(default="eu-west-1")
    COGNITO_APP_CLIENT_ID: Optional[str] = Field(default=None)
    COGNITO_PUBLIC_KEYS: Optional[List[Dict]] = Field(default=None)
    USER_INFO_URL: Optional[str] = Field(default=None)
    LOGOUT_URL: Optional[str] = Field(default=None)

    class Config:
        env_prefix = ""
        case_sentive = False
        env_file = abspath(join(dirname(__file__), "..", "..", ".env"))
        env_file_encoding = "utf-8"


cfg = WebappConfig()
