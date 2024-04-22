from . import data
from logger import logger
from app.backend.classes.ConfigProductLoader import ConfigProductLoader


def initialize(hostname, **kwargs):
    logger.debug("Loading reference data...")
    data.load_refdata(hostname=hostname, **kwargs)
    logger.debug("Loading configuration data...")
    data.load_config(hostname=hostname, **kwargs)
    logger.debug("Product loader...")
    loader = ConfigProductLoader(data)
    loader.save_to_db()
    logger.debug("Complete...")


if __name__ == "__main__":
    initialize()
