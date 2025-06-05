from typing import Optional, Sequence

from django.http import (
    HttpResponse, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError
)

from main.core.domain.ports.repositories.response_repository import ResponseRepository


class DjangoResponseAdapter(ResponseRepository):
    CONTENT_TYPE = "text/plain; charset=utf-8"

    def success(self, content: str, status: int = 200) -> HttpResponse:
        return HttpResponse(
            content,
            status=status,
            content_type=self.CONTENT_TYPE
        )

    def forbidden(self, content: str) -> HttpResponseForbidden:
        return HttpResponseForbidden(
            content,
            content_type=self.CONTENT_TYPE
        )

    def conflict(self, content: str) -> HttpResponseForbidden:
        return HttpResponseForbidden(
            content,
            content_type=self.CONTENT_TYPE,
            status=409
        )

    def not_found(self, content: str) -> HttpResponseNotFound:
        return HttpResponseNotFound(
            content,
            content_type=self.CONTENT_TYPE
        )

    def method_not_allowed(
            self,
            permitted_methods: Sequence[str],
            content: Optional[str] = None
    ) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(
            permitted_methods,
            content,
            content_type=self.CONTENT_TYPE
        )

    def bad_request(self, content: str) -> HttpResponseBadRequest:
        return HttpResponseBadRequest(
            content,
            content_type=self.CONTENT_TYPE
        )

    def server_error(self, content: str) -> HttpResponseServerError:
        return HttpResponseServerError(
            content,
            content_type=self.CONTENT_TYPE
        )

    def technical_error(self, content: str) -> HttpResponseServerError:
        return HttpResponseServerError(
            content,
            content_type=self.CONTENT_TYPE,
            status=503
        )
