from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Api

db = SQLAlchemy(engine_options={"fast_executemany": True})
ma = Marshmallow()
api = Api(doc='/api/doc/')
