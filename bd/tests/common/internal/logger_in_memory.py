from typing import Any

from main.domain.ports.repositories.logger_repository import LoggerRepository


class LoggerInMemory(LoggerRepository):
    def info(self, message: str, **kwargs: Any) -> None:
        print(message)

    def warning(self, message: str, **kwargs: Any) -> None:
        print(message)

    def error(self, message: str, **kwargs: Any) -> None:
        print(message)

    def debug(self, message: str, **kwargs: Any) -> None:
        print(message)
