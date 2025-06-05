from typing import Optional

from django.http import HttpResponseForbidden

from main.domain.ports.repositories.authorization_repository import AuthorizationRepository


class AuthorizationService:
    def __init__(self, auth_port: AuthorizationRepository):
        self._auth_port = auth_port

    def verify_token(self, auth_token: Optional[str]) -> Optional[HttpResponseForbidden]:
        return self._auth_port.verify_token(auth_token)
