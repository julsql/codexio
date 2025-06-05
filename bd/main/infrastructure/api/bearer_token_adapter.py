from typing import Optional

from django.http import HttpResponseForbidden

from main.domain.ports.repositories.authorization_repository import AuthorizationRepository
from main.domain.ports.repositories.reponse_repository import ResponseRepository


class BearerTokenAdapter(AuthorizationRepository):
    def __init__(self, response_adapter: ResponseRepository, valid_token: str):
        self._valid_token = valid_token
        self.response_adapter = response_adapter

    def verify_token(self, auth_token: Optional[str]) -> Optional[HttpResponseForbidden]:
        if not auth_token or auth_token != f"Bearer {self._valid_token}":
            return self.response_adapter.forbidden("Vous n'avez pas l'autorisation")
        return None
