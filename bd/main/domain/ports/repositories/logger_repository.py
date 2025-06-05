from abc import ABC, abstractmethod
from typing import Any


class LoggerRepository(ABC):
    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        pass
