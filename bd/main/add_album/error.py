import os
from main.core.common.logger import logger


class Error(Exception):

    def __init__(self, message_log, isbn=None):
        __FILEPATH__ = os.path.dirname(os.path.abspath(__file__))

        logger.info(message_log, extra={"isbn": isbn})
        super().__init__(message_log)
