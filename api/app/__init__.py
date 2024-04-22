import os
from flask import Flask
from sqlalchemy import event
from dotenv import load_dotenv
from config import CONFIG

from app.extensions import init_extensions
from app.shared import bind_namespaces
from app.auth import set_db_user_id

load_dotenv()


def create_app(env="DEV"):
    config = CONFIG.get(env)
    app = Flask(__name__)
    app.config.from_object(config)

    app, db, _, api, _ = init_extensions(app)
    with app.app_context():
        # bind routes
        from .route_registration import NAMESPACES, RPC_NAMESPACES, base_bp

        app.register_blueprint(base_bp)
        bind_namespaces(api, NAMESPACES, "/api")
        bind_namespaces(api, RPC_NAMESPACES, "/rpc")

        event.listens_for(db.session, "after_begin")(set_db_user_id)
        db.metadata.reflect(bind=db.engine)

    print("Successfully started app...")
    return app
