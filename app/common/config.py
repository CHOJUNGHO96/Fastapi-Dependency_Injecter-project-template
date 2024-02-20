from os import environ, path

from pydantic_settings import BaseSettings


class MainConfig(BaseSettings):
    """
    기본 Config값
    """

    BASE_DIR: str = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), "app")

    DEBUG: bool = False

    # BASE
    PROJECT_NAME: str = "CJH_FASTAPI_TEMPLATE"
    VERSION: str = "1.0.0"

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    # DB
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = False
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # REDIS
    REDIS_PORT: int
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_EXPIRE_TIME: int = 86400

    # RABBITMQ
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_ID: str
    RABBITMQ_PASSWORD: str

    # TDD
    TEST_MODE: bool = False
    # TEST_DB_URL: str

    class Config:
        env_prefix = ""  # 환경 변수 접두사 설정 (ex. "API_")


class LocalConfig(MainConfig):
    """
    로컬환경 Config값
    """

    TRUSTED_HOSTS: list[str] = ["*"]
    ALLOW_SITE: list[str] = ["*"]
    DB_ECHO: bool = False
    DEBUG: bool = True


class ProdConfig(MainConfig):
    """
    운영환경 Config값
    """

    TRUSTED_HOSTS: list[str] = ["*"]
    ALLOW_SITE: list[str] = ["*"]


class TestConfig(MainConfig):
    """
    테스트환경 Config값
    """

    ALLOW_SITE: list[str] = ["*"]
    TEST_MODE: bool = True
    DB_ECHO: bool = False


def get_config():
    """
    환경변수에 따른 Config 반환
    """
    config = dict(prod=ProdConfig, test=TestConfig, local=LocalConfig)
    return config[environ.get("API_MODE", "local")]()
