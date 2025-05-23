from main.core.common.logger.logger import logger


class SheetError(Exception):

    def __init__(self, message_log: str) -> None:
        logger.info(message_log)
        super().__init__(message_log)
