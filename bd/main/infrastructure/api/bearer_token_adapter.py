from typing import Optional

from main.core.common.reponse.utf8_response import UTF8ResponseForbidden
from main.domain.ports.repositories.authorization_repository import AuthorizationRepository


class BearerTokenAdapter(AuthorizationRepository):
    def __init__(self, valid_token: str):
        self._valid_token = valid_token

    def verify_token(self, auth_token: Optional[str]) -> Optional[UTF8ResponseForbidden]:
        if not auth_token or auth_token != f"Bearer {self._valid_token}":
            return UTF8ResponseForbidden("Vous n'avez pas l'autorisation")
        return None
