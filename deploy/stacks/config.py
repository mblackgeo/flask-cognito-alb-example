from os.path import abspath, dirname, join

from pydantic import BaseSettings, Field


class CDKConfig(BaseSettings):
    NAMESPACE: str = Field(default="webapp")
    ENV: str = Field(default="prod")

    AWS_REGION: str = Field(default="eu-west-1")
    AWS_ACCOUNT: str = Field(...)

    SUBDOMAIN: str = Field(default="webapp")
    DOMAIN: str = Field(default="sparkgeo.uk")
    AUTH_SUBDOMAIN: str = Field(default="webapp-auth")

    FARGATE_CPU: int = Field(default=256)
    FARGATE_MEM: int = Field(default=512)
    FARGATE_PORT: int = Field(default=1000)

    class Config:
        env_prefix = ""
        case_sentive = False
        env_file = abspath(join(dirname(__file__), "..", "..", ".env"))
        env_file_encoding = "utf-8"


cfg = CDKConfig()
