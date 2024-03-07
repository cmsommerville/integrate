import os
from dotenv import load_dotenv
from redis import Redis
from sqlalchemy.engine import URL

load_dotenv()


connection_url = URL.create(
    drivername="mssql+pyodbc",
    username=os.getenv("DEV_DATABASE_UID"),
    password=os.getenv("DEV_DATABASE_PWD"),
    host=os.getenv("DEV_DATABASE_SERVER"),
    port=os.getenv("DEV_DATABASE_PORT"),
    database=os.getenv("DEV_DATABASE_DB"),
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "TrustServerCertificate": "yes",
    },
)


class BaseConfig:
    PROPAGATE_EXCEPTIONS = True
    PERMANENT_SESSION_LIFETIME = 3600
    SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
    SESSION_TYPE = os.getenv("SESSION_TYPE")
    SESSION_REDIS = Redis(host="127.0.0.1", port=6379, db=0)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    SUPPORT_TEMPORAL_TABLES = True


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = connection_url
    DB_USER_NAME = os.getenv("DEV_DATABASE_UID")


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_SQLALCHEMY_DATABASE_URI")
    DB_USER_NAME = os.getenv("DEV_DATABASE_UID")


CONFIG = {"DEV": DevConfig(), "TEST": TestConfig()}
