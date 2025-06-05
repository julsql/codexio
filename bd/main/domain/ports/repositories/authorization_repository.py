from abc import ABC, abstractmethod
from typing import Optional

from main.core.common.reponse.utf8_response import UTF8ResponseForbidden


class AuthorizationRepository(ABC):
    @abstractmethod
    def verify_token(self, auth_token: Optional[str]) -> Optional[UTF8ResponseForbidden]:
        pass
