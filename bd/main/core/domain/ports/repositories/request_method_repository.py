from abc import ABC, abstractmethod
from typing import Optional

from django.http import HttpResponseNotAllowed


class RequestMethodRepository(ABC):
    @abstractmethod
    def method_not_allowed(self, method: str, expected_auth_method: str) -> Optional[HttpResponseNotAllowed]:
        pass
