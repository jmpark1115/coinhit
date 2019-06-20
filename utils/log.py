import logging
from market_maker.settings import settings


def setup_custom_logger(name, log_level=settings.LOG_LEVEL):
    # formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    # formatter = logging.Formatter(fmt='%(asctime)s-%(module)s-%(message)s')
    formatter = logging.Formatter(fmt='%(module)s-%(lineno)s-%(message)s')
    # formatter = logging.Formatter(fmt='%(asctime)s - %(filename)s - %(lineno)s- %(module)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger
