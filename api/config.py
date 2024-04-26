import os
from redis import Redis
from sqlalchemy.engine import URL


connection_url = URL.create(
    drivername="mssql+pyodbc",
    username=os.getenv("DATABASE_UID"),
    password=os.getenv("DATABASE_PWD"),
    host=os.getenv("DATABASE_SERVER"),
    port=os.getenv("DATABASE_PORT"),
    database=os.getenv("DATABASE_DB"),
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        # "TrustServerCertificate": "yes",
    },
)


class BaseConfig:
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    PROPAGATE_EXCEPTIONS = True
    PERMANENT_SESSION_LIFETIME = 3600
    SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
    SESSION_TYPE = os.getenv("SESSION_TYPE")
    SESSION_REDIS = Redis(
        host=os.getenv("REDIS_HOST", "127.0.0.1"),
        port=os.getenv("REDIS_PORT", 6379),
        db=0,
    )
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    SUPPORT_TEMPORAL_TABLES = True


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = connection_url
    DB_USER_NAME = os.getenv("DATABASE_UID")


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_SQLALCHEMY_DATABASE_URI")
    DB_USER_NAME = os.getenv("DATABASE_UID")


class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = connection_url
    DB_USER_NAME = os.getenv("DATABASE_UID")


CONFIG = {"DEV": DevConfig(), "TEST": TestConfig(), "PROD": ProdConfig()}
