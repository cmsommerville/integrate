import os
from flask import Flask
from flask_cors import CORS
from flask_restx import Resource
from dotenv import load_dotenv

from app.extensions import db, ma, api
from app.shared import bind_namespaces

load_dotenv()        

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, supports_credentials=True)

    db.init_app(app)
    ma.init_app(app)
    app.config["SESSION_SQLALCHEMY"] = db

    api.init_app(app)

    from .route_registration import NAMESPACES
    bind_namespaces(api, NAMESPACES, '/api')

    @app.route('/test')
    def tester(): 
        from sqlalchemy.inspection import inspect
        from app.backend.models import Model_ConfigAgeBandSet

        for k, v in inspect(Model_ConfigAgeBandSet).relationships.items():
            print(f"{v.relationship_code}")
        return {"hello": "world"}, 200

    return app
