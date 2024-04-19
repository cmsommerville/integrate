import redis
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_session import Session
from flask_migrate import Migrate

metadata = MetaData(schema="dbo")
db = SQLAlchemy(metadata=metadata, engine_options={"fast_executemany": True})
migrate = Migrate()
ma = Marshmallow()
api = Api(doc="/api/doc/")
sess = Session()
cache = redis.Redis(db=1)
