from abc import ABC, abstractmethod
from typing import Optional

from main.core.common.reponse.utf8_response import UTF8ResponseNotAllowed


class RequestMethodRepository(ABC):
    @abstractmethod
    def method_not_allowed(self, method: str, expected_auth_method: str) -> Optional[UTF8ResponseNotAllowed]:
        pass
