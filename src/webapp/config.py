"""App configuration."""

from os import urandom
from os.path import abspath, dirname, join
from typing import Optional

from pydantic import BaseSettings, Field


class WebappConfig(BaseSettings):
    SECRET_KEY: Optional[str] = Field(default=str(urandom(32)))
    FLASK_APP: Optional[str] = Field(defauly="webapp")
    FLASK_ENV: Optional[str] = Field(default="dev")

    class Config:
        env_prefix = ""
        case_sentive = False
        env_file = abspath(join(dirname(__file__), "..", "..", ".env"))
        env_file_encoding = "utf-8"
