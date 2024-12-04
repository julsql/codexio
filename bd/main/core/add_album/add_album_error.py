from main.core.common.logger.logger import logger

class AddAlbumError(Exception):

    def __init__(self, message_log: str, isbn: int = None) -> None:
        logger.info(message_log, extra={"isbn": isbn})
        super().__init__(message_log)
