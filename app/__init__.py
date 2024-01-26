from flask import Flask
from flask_cors import CORS
from sqlalchemy import event
from dotenv import load_dotenv

from app.extensions import db, ma, api, sess
from app.shared import bind_namespaces
from app.auth import set_db_user_id

load_dotenv()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, supports_credentials=True)

    db.init_app(app)
    ma.init_app(app)
    app.config["SESSION_SQLALCHEMY"] = db

    api.init_app(app)
    sess.init_app(app)

    # bind routes
    from .route_registration import NAMESPACES

    bind_namespaces(api, NAMESPACES, "/api")

    event.listens_for(db.session, "after_begin")(set_db_user_id)

    return app
