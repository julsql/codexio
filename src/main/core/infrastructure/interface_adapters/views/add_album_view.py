from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, \
    HttpResponseServerError

from main.core.application.usecases.add_album.add_bd_service import AddBdService
from main.core.application.usecases.add_album.add_book_service import AddBookService
from main.core.application.usecases.authorization.authorization_service import AuthorizationService
from main.core.domain.exceptions.album_exceptions import AlbumNotFoundException, AlbumAlreadyExistsException, \
    AlbumSourcesUnavailableException
from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.api.album_repositories_factory import build_album_repositories
from main.core.infrastructure.interface_adapters.bearer_token.bearer_token_adapter import BearerTokenAdapter
from main.core.infrastructure.interface_adapters.profile_type.profile_type_adapter import ProfileTypeAdapter
from main.core.infrastructure.interface_adapters.request_methods.request_method_adapter import RequestMethodAdapter
from main.core.infrastructure.interface_adapters.responses.api_response_adapter import ApiResponseAdapter
from main.core.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.core.infrastructure.persistence.database.models import Collection
from main.core.infrastructure.persistence.sheet.sheet_adapter import SheetAdapter


class AddAlbumView:
    def __init__(self):
        self.logger_adapter = PythonLoggerAdapter()
        self.response_adapter = ApiResponseAdapter()
        self.request_method_adapter = RequestMethodAdapter(self.response_adapter)
        self.profile_type_adapter = ProfileTypeAdapter(self.response_adapter)
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
            sheet_repository = SheetAdapter(collection.doc_id, collection.sheet_name)

            profile_type = self.profile_type_adapter.get_profile_type(collection)
            if not isinstance(profile_type, ProfileType):
                return profile_type

            repositories = build_album_repositories(profile_type, self.logger_adapter)
            if not repositories:
                return self.response_adapter.technical_error("Erreur dans la recherche de profils")

            if profile_type == ProfileType.BD:
                service = AddBdService(repositories,
                                       sheet_repository,
                                       self.logger_adapter)
            else:
                service = AddBookService(
                    repositories,
                    sheet_repository,
                    self.logger_adapter,
                )
            service.main(isbn)

            return self.response_adapter.success(f'Album {int(isbn)} ajouté avec succès')

        except AlbumSourcesUnavailableException as e:
            self.logger_adapter.error(str(e), isbn=isbn)
            return self.response_adapter.technical_error(
                "Sources indisponibles : " + ", ".join(e.sources)
            )

        except AlbumNotFoundException as e:
            self.logger_adapter.warning(str(e), extra={"isbn": isbn})
            return self.response_adapter.not_found(f"Album {int(isbn)} introuvable")

        except AlbumAlreadyExistsException as e:
            self.logger_adapter.info(str(e), extra={"isbn": isbn})
            return self.response_adapter.conflict(f"L'album {int(isbn)} existe déjà")

        except Exception as e:
            self.logger_adapter.error(str(e), extra={"isbn": isbn})
            return self.response_adapter.server_error("Erreur interne")


def add_album(request: HttpRequest,
              isbn: int) -> HttpResponse | HttpResponseForbidden | HttpResponseNotFound | HttpResponseBadRequest | HttpResponseServerError:
    view = AddAlbumView()
    return view.handle_request(request, isbn)
