import os
from app import create_app
from config import CONFIG

from werkzeug.middleware.profiler import ProfilerMiddleware


if __name__ == "__main__":
    ENV = os.getenv("ENV")
    config = CONFIG.get(ENV)
    app = create_app(config)
    app.config["PROFILE"] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[20])
    app.run(host="127.0.0.1", port=5000, debug=True)
