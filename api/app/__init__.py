from flask import Flask
from flask_cors import CORS
from sqlalchemy import event
from dotenv import load_dotenv
from config import CONFIG

from app.extensions import db, ma, api, sess, migrate
from app.shared import bind_namespaces, BaseReflectedModel
from app.auth import set_db_user_id

load_dotenv()


def create_app(env="DEV"):
    config = CONFIG.get(env)
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, supports_credentials=True)

    db.init_app(app)
    ma.init_app(app)
    app.config["SESSION_SQLALCHEMY"] = db

    api.init_app(app)
    sess.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # bind routes
        from .route_registration import NAMESPACES, RPC_NAMESPACES

        bind_namespaces(api, NAMESPACES, "/api")
        bind_namespaces(api, RPC_NAMESPACES, "/rpc")

        event.listens_for(db.session, "after_begin")(set_db_user_id)
        # db.metadata.reflect(db.engine)
        db.metadata.reflect(bind=db.engine)

    return app
