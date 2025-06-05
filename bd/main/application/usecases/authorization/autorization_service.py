from typing import Optional

from main.core.common.reponse.utf8_response import UTF8ResponseForbidden
from main.domain.ports.repositories.authorization_repository import AuthorizationRepository


class AuthorizationService:
    def __init__(self, auth_port: AuthorizationRepository):
        self._auth_port = auth_port

    def verify_token(self, auth_token: Optional[str]) -> Optional[UTF8ResponseForbidden]:
        return self._auth_port.verify_token(auth_token)
