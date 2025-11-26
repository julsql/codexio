from abc import ABC, abstractmethod
from typing import Optional

from django.http import HttpResponseForbidden

from main.core.infrastructure.persistence.database.models import Collection


class AuthorizationRepository(ABC):
    @abstractmethod
    def verify_token(self, auth_header: Optional[str]) -> Collection | HttpResponseForbidden:
        pass
