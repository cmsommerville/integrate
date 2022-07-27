import os
from app import create_app
from config import CONFIG


if __name__ == "__main__":
    ENV = os.getenv("ENV")
    config = CONFIG.get(ENV)
    app = create_app(config)
    app.run(host="127.0.0.1", port=5000, debug=True)
