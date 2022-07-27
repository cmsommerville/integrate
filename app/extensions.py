# from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Api

# sess = Session()
db = SQLAlchemy(engine_options={"fast_executemany": True})
ma = Marshmallow()
api = Api()
