import time
from typing import Callable, TypeVar

T = TypeVar("T")


class HttpRetryService:
    """Rejoue un appel réseau quand l'hôte coupe la connexion ou ne répond pas à temps"""

    DEFAULT_ATTEMPTS = 3
    DEFAULT_BACKOFF_SECONDS = 1.0

    @staticmethod
    def call(operation: Callable[[], T],
             retryable: tuple[type[BaseException], ...],
             attempts: int = DEFAULT_ATTEMPTS,
             backoff_seconds: float = DEFAULT_BACKOFF_SECONDS) -> T:
        last_error: BaseException | None = None

        for attempt in range(attempts):
            try:
                return operation()
            except retryable as e:
                last_error = e
                if attempt < attempts - 1:
                    time.sleep(backoff_seconds * (2 ** attempt))

        raise last_error


class TransientHttpError(Exception):
    """Réponse que l'hôte renvoie par intermittence (challenge anti-bot, indisponibilité)"""
