import logging
import os
from typing import Any

from config.settings import LOGS_FILE
from main.domain.ports.repositories.logger_repository import LoggerRepository


class PythonLoggerAdapter(LoggerRepository):
    def __init__(self) -> None:
        self._logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("app_logger")

        if not logger.handlers:  # Éviter les handlers doubles
            os.makedirs(os.path.dirname(LOGS_FILE), exist_ok=True)

            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            file_handler = logging.FileHandler(LOGS_FILE)
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.setLevel(logging.DEBUG)

        return logger

    def _format_message(self, message: str, **kwargs: Any) -> str:
        isbn = kwargs.get('isbn')
        return f"{message} - {isbn}" if isbn else message

    def info(self, message: str, **kwargs: Any) -> None:
        self._logger.info(self._format_message(message, **kwargs))

    def warning(self, message: str, **kwargs: Any) -> None:
        self._logger.warning(self._format_message(message, **kwargs))

    def error(self, message: str, **kwargs: Any) -> None:
        self._logger.error(self._format_message(message, **kwargs))

    def debug(self, message: str, **kwargs: Any) -> None:
        self._logger.debug(self._format_message(message, **kwargs))
