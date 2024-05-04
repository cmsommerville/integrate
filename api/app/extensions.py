import redis
from flask import Flask
from sqlalchemy import MetaData
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_session import Session
from flask_migrate import Migrate
from celery import Celery, Task


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


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
