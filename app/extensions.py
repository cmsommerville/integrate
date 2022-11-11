from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_session import Session
from flask_jwt_extended import JWTManager

db = SQLAlchemy(engine_options={"fast_executemany": True})
ma = Marshmallow()
api = Api(doc='/api/doc/')
jwt = JWTManager()
sess = Session()