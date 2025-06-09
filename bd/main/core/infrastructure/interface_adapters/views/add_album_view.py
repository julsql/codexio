from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, \
    HttpResponseServerError

from main.core.application.usecases.add_album.add_album_service import AddAlbumService
from main.core.application.usecases.authorization.authorization_service import AuthorizationService
from main.core.domain.exceptions.album_exceptions import AlbumNotFoundException, AlbumAlreadyExistsException
from main.core.infrastructure.api.bd_gest_adapter import BdGestAdapter
from main.core.infrastructure.api.bd_phile_adapter import BdPhileAdapter
from main.core.infrastructure.interface_adapters.bearer_token.bearer_token_adapter import BearerTokenAdapter
from main.core.infrastructure.interface_adapters.request_methods.request_method_adapter import RequestMethodAdapter
from main.core.infrastructure.interface_adapters.responses.django_response_adapter import DjangoResponseAdapter
from main.core.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.core.infrastructure.persistence.database.models import Collection
from main.core.infrastructure.persistence.sheet.sheet_adapter import SheetAdapter


class AddAlbumView:
    def __init__(self):
        self.logger_adapter = PythonLoggerAdapter()
        self.response_adapter = DjangoResponseAdapter()
        self.request_method_adapter = RequestMethodAdapter(self.response_adapter)
        self.auth_service = AuthorizationService(
            BearerTokenAdapter(self.response_adapter)
        )

    def handle_request(self, request: HttpRequest,
                       isbn: int) -> HttpResponse | HttpResponseForbidden | HttpResponseNotFound | HttpResponseBadRequest | HttpResponseServerError:

        if method_not_allowed := self.request_method_adapter.method_not_allowed(request.method, "GET"):
            return method_not_allowed

        collection = self.auth_service.verify_token(request.headers.get('Authorization'))
        if not isinstance(collection, Collection):
            return collection

        try:
            sheet_repository = SheetAdapter(collection.doc_name, collection.sheet_name)
            bdphile_repository = BdPhileAdapter(self.logger_adapter)
            bdgest_repository = BdGestAdapter(self.logger_adapter)
            service = AddAlbumService([bdphile_repository, bdgest_repository],
                                      sheet_repository,
                                      self.logger_adapter)
            service.main(isbn)
            return self.response_adapter.success(f'Album {isbn} ajouté avec succès')

        except AlbumNotFoundException as e:
            self.logger_adapter.warning(str(e), extra={"isbn": isbn})
            return self.response_adapter.not_found(str(e))

        except AlbumAlreadyExistsException as e:
            self.logger_adapter.info(str(e), extra={"isbn": isbn})
            return self.response_adapter.conflict(str(e))

        except Exception as e:
            self.logger_adapter.error(str(e))
            return self.response_adapter.server_error("Erreur interne")


def add_album(request: HttpRequest,
              isbn: int) -> HttpResponse | HttpResponseForbidden | HttpResponseNotFound | HttpResponseBadRequest | HttpResponseServerError:
    view = AddAlbumView()
    return view.handle_request(request, isbn)
