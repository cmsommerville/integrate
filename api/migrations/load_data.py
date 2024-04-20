from . import data
from logger import logger
from app.backend.classes.ConfigProductLoader import ConfigProductLoader


def initialize():
    logger.debug("Loading reference data...")
    data.load_refdata()
    logger.debug("Loading configuration data...")
    data.load_config()
    logger.debug("Product loader...")
    loader = ConfigProductLoader(data)
    loader.save_to_db()
    logger.debug("Complete...")


if __name__ == "__main__":
    initialize()
