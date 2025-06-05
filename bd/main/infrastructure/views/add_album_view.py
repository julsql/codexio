from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, \
    HttpResponseServerError

from config.settings import POST_TOKEN
from main.application.usecases.add_album.add_album_service import AddAlbumService
from main.application.usecases.authorization.autorization_service import AuthorizationService
from main.application.usecases.request_method.request_method_service import RequestMethodService
from main.domain.exceptions.album_exceptions import AlbumNotFoundException, AlbumAlreadyExistsException
from main.infrastructure.api.bd_gest_adapter import BdGestAdapter
from main.infrastructure.api.bd_phile_adapter import BdPhileAdapter
from main.infrastructure.api.bearer_token_adapter import BearerTokenAdapter
from main.infrastructure.api.request_method_adapter import RequestMethodAdapter
from main.infrastructure.exceptions.repository_exceptions import InfrastructureException
from main.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.infrastructure.persistence.sheet.sheet_adapter import SheetAdapter
from main.infrastructure.responses.django_response_adapter import DjangoResponseAdapter


class AddAlbumView:
    def __init__(self):
        self.logger_adapter = PythonLoggerAdapter()
        self.response_adapter = DjangoResponseAdapter()
        self.request_method_service = RequestMethodService(RequestMethodAdapter(self.response_adapter))
        self.auth_service = AuthorizationService(
            BearerTokenAdapter(self.response_adapter, POST_TOKEN)
        )

    def handle_request(self, request: HttpRequest,
                       isbn: int) -> HttpResponse | HttpResponseForbidden | HttpResponseNotFound | HttpResponseBadRequest | HttpResponseServerError:

        if method_not_allowed := self.request_method_service.method_not_allowed(request.method, "GET"):
            return method_not_allowed

        if token_invalid := self.auth_service.verify_token(request.headers.get('Authorization')):
            return token_invalid

        try:
            sheet_repository = SheetAdapter()
            bdphile_repository = BdPhileAdapter(self.logger_adapter)
            bdgest_repository = BdGestAdapter(self.logger_adapter)
            service = AddAlbumService([bdphile_repository, bdgest_repository], sheet_repository, self.logger_adapter)
            service.main(isbn)
            return self.response_adapter.success(f'Album {isbn} ajouté avec succès')

        except AlbumNotFoundException as e:
            self.logger_adapter.warning(str(e), extra={"isbn": isbn})
            return self.response_adapter.not_found(str(e))

        except AlbumAlreadyExistsException as e:
            self.logger_adapter.info(str(e), extra={"isbn": isbn})
            return self.response_adapter.conflict(str(e))

        except InfrastructureException as e:
            self.logger_adapter.error(str(e))
            return self.response_adapter.technical_error("Erreur technique")

        except Exception as e:
            self.logger_adapter.error(str(e))
            return self.response_adapter.server_error("Erreur interne")


def add_album(request: HttpRequest,
              isbn: int) -> HttpResponse | HttpResponseForbidden | HttpResponseNotFound | HttpResponseBadRequest | HttpResponseServerError:
    view = AddAlbumView()
    return view.handle_request(request, isbn)
