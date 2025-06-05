from typing import Optional

from main.core.common.reponse.utf8_response import UTF8ResponseNotAllowed
from main.domain.ports.repositories.request_method_repository import RequestMethodRepository


class RequestMethodService:
    def __init__(self, auth_method: RequestMethodRepository):
        self.auth_method = auth_method

    def method_not_allowed(self, auth_method: str, expected_auth_method: str) -> Optional[UTF8ResponseNotAllowed]:
        return self.auth_method.method_not_allowed(auth_method, expected_auth_method)
