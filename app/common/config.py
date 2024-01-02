from dataclasses import dataclass
from os import environ, path

from app.util.config_decrypt import decrypt_config


@dataclass
class MainConfig:
    """
    기본 Config값
    """

    # Config 파일 복호화
    file_path = path.join(path.dirname(path.abspath(__file__)))
    json_data = decrypt_config(file_path)

    # 경로
    BASE_DIR: str = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), "app")

    # JWT
    JWT_SECRET_KEY: str = json_data["JWT"]["SECRET_KEY"]
    JWT_ALGORITHM: str = json_data["JWT"]["ALGORITHM"]
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = json_data["JWT"]["ACCESS_TOKEN_EXPIRE_MINUTES"]

    # DB
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = False
    DEBUG: bool = False
    DB_URL: str = f"postgresql+asyncpg://{json_data['DB']['POSTGRES']['USER']}:{json_data['DB']['POSTGRES']['PASSWD']}@{json_data['DB']['POSTGRES']['HOST']}:{json_data['DB']['POSTGRES']['PORT']}/{json_data['DB']['POSTGRES']['NAME']}"

    # REDIS
    REDIS_PORT: str = json_data["DB"]["REDIS"]["REDIS_PORT"]
    REDIS_HOST: str = json_data["DB"]["REDIS"]["REDIS_HOST"]
    REDIS_PASSWORD: str = json_data["DB"]["REDIS"]["REDIS_PASSWORD"]
    REDIS_EXPIRE_TIME: int = 86400

    # TDD
    TEST_MODE: bool = False
    TEST_DB_URL: str = f"postgresql+asyncpg://{json_data['DB']['POSTGRES']['USER']}:{json_data['DB']['POSTGRES']['PASSWD']}@{json_data['DB']['POSTGRES']['HOST']}:{json_data['DB']['POSTGRES']['PORT']}/{json_data['DB']['POSTGRES']['TEST_DB_NAME']}"


@dataclass
class LocalConfig(MainConfig):
    """
    로컬환경 Config값
    """

    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DB_ECHO: bool = False
    DEBUG: bool = True


@dataclass
class ProdConfig(MainConfig):
    """
    운영환경 Config값
    """

    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


@dataclass
class TestConfig(MainConfig):
    """
    테스트환경 Config값
    """

    DB_URL: str = MainConfig.TEST_DB_URL
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True
    DB_ECHO: bool = False


def get_config():
    """
    환경변수에 따른 Config 반환
    :return:
    """
    config = dict(prod=ProdConfig, test=TestConfig, local=LocalConfig)
    return config[environ.get("CJH_API_MODE", "local")]()
