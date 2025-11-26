from typing import Optional

from django.http import HttpResponseForbidden

from main.core.domain.ports.repositories.authorization_repository import AuthorizationRepository
from main.core.domain.ports.repositories.response_repository import ResponseRepository
from main.core.infrastructure.persistence.database.models import Collection


class BearerTokenAdapter(AuthorizationRepository):
    def __init__(self, response_adapter: ResponseRepository):
        self.response_adapter = response_adapter

    def verify_token(self, auth_header: Optional[str]) -> Collection | HttpResponseForbidden:
        if not auth_header or not auth_header.startswith('Bearer '):
            return self.response_adapter.forbidden("Autorisation manquante ou invalide")

        token = auth_header.split('Bearer ')[1].strip()

        try:
            collection = Collection.objects.get(token=token)
            return collection
        except Collection.DoesNotExist:
            return self.response_adapter.forbidden("Vous n'avez pas l'autorisation")
