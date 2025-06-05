from typing import Optional

from main.core.common.reponse.utf8_response import UTF8ResponseNotAllowed
from main.domain.ports.repositories.request_method_repository import RequestMethodRepository


class RequestMethodAdapter(RequestMethodRepository):
    def method_not_allowed(self, method: str, expected_auth_method: str) -> Optional[UTF8ResponseNotAllowed]:
        if method != expected_auth_method:
            return UTF8ResponseNotAllowed([expected_auth_method], f"Il faut une requête {expected_auth_method}")
        return None
