import logging

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logger = logging.getLogger("Some logger")
file_handler = logging.FileHandler("some_logger.log")
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info("Info message")
logger.warning("Warning message")
