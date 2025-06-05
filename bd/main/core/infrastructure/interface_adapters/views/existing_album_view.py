from django.http import HttpRequest, HttpResponse, HttpResponseServerError

from config.settings import POST_TOKEN
from main.core.application.usecases.authorization.authorization_service import AuthorizationService
from main.core.application.usecases.existing_album.existing_album_service import ExistingAlbumService
from main.core.infrastructure.interface_adapters.bearer_token.bearer_token_adapter import BearerTokenAdapter
from main.core.infrastructure.interface_adapters.request_methods.request_method_adapter import RequestMethodAdapter
from main.core.infrastructure.interface_adapters.responses.django_response_adapter import DjangoResponseAdapter
from main.core.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.core.infrastructure.persistence.sheet.sheet_adapter import SheetAdapter


class ExistingAlbumView:
    def __init__(self):
        self.logger_adapter = PythonLoggerAdapter()
        self.response_adapter = DjangoResponseAdapter()
        self.request_method_adapter = RequestMethodAdapter(self.response_adapter)
        self.auth_service = AuthorizationService(
            BearerTokenAdapter(self.response_adapter, POST_TOKEN)
        )

    def handle_request(self, request: HttpRequest,
                       isbn: int) -> HttpResponse | HttpResponseServerError:

        if method_not_allowed := self.request_method_adapter.method_not_allowed(request.method, "GET"):
            return method_not_allowed

        if token_invalid := self.auth_service.verify_token(request.headers.get('Authorization')):
            return token_invalid

        try:
            sheet_repository = SheetAdapter()
            service = ExistingAlbumService(sheet_repository)
            if service.execute(isbn):
                message = f"Album {isbn} déjà enregistré"
            else:
                message = f"Album {isbn} jamais enregistré"
            return self.response_adapter.success(message)

        except Exception as e:
            self.logger_adapter.error(str(e))
            return self.response_adapter.server_error("Erreur interne")


def existing_album(request: HttpRequest,
                   isbn: int) -> HttpResponse | HttpResponseServerError:
    view = ExistingAlbumView()
    return view.handle_request(request, isbn)
