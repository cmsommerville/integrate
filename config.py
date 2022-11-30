import os
import urllib
from dotenv import load_dotenv
from redis import Redis

load_dotenv()

SQL_SERVER_CONNECTION_STRING = "Server={SERVER};Database={DB};UID={UID};PWD={PWD};"
SQL_SERVER_CONNECTION_STRING = "Driver={ODBC Driver 17 for SQL Server};" + SQL_SERVER_CONNECTION_STRING.format(**{
    "SERVER": os.getenv('DEV_DATABASE_SERVER'), 
    "DB": os.getenv('DEV_DATABASE_DB'), 
    "UID": os.getenv('DEV_DATABASE_UID'),
    "PWD": os.getenv('DEV_DATABASE_PWD')
})
params = urllib.parse.quote_plus(SQL_SERVER_CONNECTION_STRING)


class BaseConfig():
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    PROPAGATE_EXCEPTIONS = True
    PERMANENT_SESSION_LIFETIME = 3600
    SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
    SESSION_TYPE = os.getenv("SESSION_TYPE")
    SESSION_REDIS = Redis(host="localhost", port=6379, db=0)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SUPPORT_TEMPORAL_TABLES = True


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    DB_USER_NAME = os.getenv('DEV_DATABASE_UID')

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_SQLALCHEMY_DATABASE_URI")
    DB_USER_NAME = os.getenv('DEV_DATABASE_UID')

CONFIG = {
    "DEV": DevConfig(),
    "TEST": TestConfig()
}
