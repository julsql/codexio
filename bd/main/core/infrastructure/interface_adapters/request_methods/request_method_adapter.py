from typing import Optional

from django.http import HttpResponseNotAllowed

from main.core.domain.ports.repositories.request_method_repository import RequestMethodRepository
from main.core.domain.ports.repositories.response_repository import ResponseRepository


class RequestMethodAdapter(RequestMethodRepository):
    def __init__(self, response_adapter: ResponseRepository):
        self.response_adapter = response_adapter

    def method_not_allowed(self, method: str, expected_auth_method: str) -> Optional[HttpResponseNotAllowed]:
        if method != expected_auth_method:
            return self.response_adapter.method_not_allowed([expected_auth_method],
                                                            f"Il faut une requête {expected_auth_method}")
        return None
