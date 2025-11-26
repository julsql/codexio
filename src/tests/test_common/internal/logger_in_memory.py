from typing import Any

from main.core.domain.ports.repositories.logger_repository import LoggerRepository


class LoggerInMemory(LoggerRepository):
    def info(self, message: str, **kwargs: Any) -> None:
        # print(message)
        pass

    def warning(self, message: str, **kwargs: Any) -> None:
        # print(message)
        pass

    def error(self, message: str, **kwargs: Any) -> None:
        # print(message)
        pass

    def debug(self, message: str, **kwargs: Any) -> None:
        # print(message)
        pass
