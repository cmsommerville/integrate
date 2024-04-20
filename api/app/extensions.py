import redis
from flask import Flask
from sqlalchemy import MetaData
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_session import Session
from flask_migrate import Migrate

cors = CORS(supports_credentials=True)
metadata = MetaData(schema="dbo")
db = SQLAlchemy(metadata=metadata, engine_options={"fast_executemany": True})
migrate = Migrate()
ma = Marshmallow()
api = Api(doc="/api/doc/")
sess = Session()
cache = redis.Redis(db=1)


def init_extensions(app: Flask):
    cors.init_app(app)

    db.init_app(app)
    ma.init_app(app)
    app.config["SESSION_SQLALCHEMY"] = db

    api.init_app(app)
    sess.init_app(app)
    migrate.init_app(app, db)

    return app, db, ma, api, sess
