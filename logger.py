import logging

logging.basicConfig(level=logging.INFO)

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler("file.log")
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")
f_format = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(pathname)s - method name: %(funcName)s - line no: %(lineno)s - %(message)s"
)
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
