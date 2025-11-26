from typing import Optional, Sequence

from django.http import (
    HttpResponse, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError, Http404
)

from main.core.domain.ports.repositories.response_repository import ResponseRepository


class RequestResponseAdapter(ResponseRepository):
    CONTENT_TYPE = "text/plain; charset=utf-8"

    def success(self, content: str, status: int = 200) -> HttpResponse:
        pass

    def forbidden(self, content: str) -> HttpResponseForbidden:
        raise Http404(content)

    def conflict(self, content: str) -> HttpResponseForbidden:
        raise Http404(content)

    def not_found(self, content: str) -> HttpResponseNotFound:
        raise Http404(content)

    def method_not_allowed(
            self,
            permitted_methods: Sequence[str],
            content: Optional[str] = None
    ) -> HttpResponseNotAllowed:
        raise Http404(content)

    def bad_request(self, content: str) -> HttpResponseBadRequest:
        raise Http404(content)

    def server_error(self, content: str) -> HttpResponseServerError:
        raise Http404(content)

    def technical_error(self, content: str) -> HttpResponseServerError:
        raise Http404(content)
