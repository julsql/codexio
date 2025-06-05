from abc import ABC, abstractmethod
from typing import Optional

from django.http import HttpResponseForbidden


class AuthorizationRepository(ABC):
    @abstractmethod
    def verify_token(self, auth_token: Optional[str]) -> Optional[HttpResponseForbidden]:
        pass
