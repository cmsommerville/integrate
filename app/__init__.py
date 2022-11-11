import os
from flask import Flask
from flask_cors import CORS
from flask_restx import Resource
from dotenv import load_dotenv
import logging
from sqlalchemy import event

# logging.basicConfig(filename='logs/info.log')
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from app.extensions import db, ma, api, sess, jwt
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
    jwt.init_app(app)
    sess.init_app(app)
    
    # bind routes
    from .route_registration import NAMESPACES
    bind_namespaces(api, NAMESPACES, '/api')

    from work.test import Resource_TestSQLJSON
    api.add_resource(Resource_TestSQLJSON, '/work/test')

    # bind subscribers
    from .subscription_registration import SUBSCRIPTIONS
    for subscription in SUBSCRIPTIONS:
        subscription.subscribe()

    import app.auth as auth

    return app
