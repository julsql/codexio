from main.core.common.logger import logger

class AddAlbumError(Exception):

    def __init__(self, message_log, isbn=None):
        logger.info(message_log, extra={"isbn": isbn})
        super().__init__(message_log)
