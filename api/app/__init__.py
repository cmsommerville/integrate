import os
from flask import Flask
from sqlalchemy import event
from config import CONFIG

from app.extensions import init_extensions, celery_init_app
from app.shared import bind_namespaces
from app.auth import set_db_user_id


def create_app():
    ENV = os.environ.get("ENV", "DEV")
    config = CONFIG.get(ENV)
    app = Flask(__name__)
    app.config.from_object(config)
    # app.config["CELERY"] = dict(
    #     broker_url=os.getenv("CELERY_BROKER_URL"),
    #     result_backend=os.getenv("CELERY_RESULT_BACKEND"),
    #     task_ignore_result=True,
    # )

    app, db, _, api, _ = init_extensions(app)

    app.config.from_prefixed_env()
    celery_init_app(app)

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
