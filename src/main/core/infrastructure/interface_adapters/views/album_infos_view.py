from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, \
    HttpResponseServerError

from main.core.application.usecases.add_album.get_infos_service import GetInfosService
from main.core.application.usecases.authorization.authorization_service import AuthorizationService
from main.core.domain.exceptions.album_exceptions import AlbumNotFoundException
from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.api.bd_fugue_adapter import BdFugueAdapter
from main.core.infrastructure.api.bd_gest_adapter import BdGestAdapter
from main.core.infrastructure.api.bd_google_adapter import BdGoogleAdapter
from main.core.infrastructure.api.bd_phile_adapter import BdPhileAdapter
from main.core.infrastructure.api.bnf_adapter import BnfAdapter
from main.core.infrastructure.api.book_adapter import BookAdapter
from main.core.infrastructure.api.open_library_adapter import OpenLibraryAdapter
from main.core.infrastructure.interface_adapters.bearer_token.bearer_token_adapter import BearerTokenAdapter
from main.core.infrastructure.interface_adapters.profile_type.profile_type_adapter import ProfileTypeAdapter
from main.core.infrastructure.interface_adapters.request_methods.request_method_adapter import RequestMethodAdapter
from main.core.infrastructure.interface_adapters.responses.api_response_adapter import ApiResponseAdapter
from main.core.infrastructure.interface_adapters.views.formatters import album_to_dict
from main.core.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.core.infrastructure.persistence.database.models import Collection


class AlbumInfosView:
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
            profile_type = self.profile_type_adapter.get_profile_type(collection)
            if not isinstance(profile_type, ProfileType):
                return profile_type

            if profile_type == ProfileType.BD:
                bdphile_repository = BdPhileAdapter(self.logger_adapter)
                bdgest_repository = BdGestAdapter(self.logger_adapter)
                bdgoogle_repository = BdGoogleAdapter(self.logger_adapter)
                bdfugue_repository = BdFugueAdapter(self.logger_adapter)
                service = GetInfosService(
                    [bdphile_repository, bdgest_repository, bdfugue_repository, bdgoogle_repository],
                    self.logger_adapter)
            elif profile_type == ProfileType.BOOK:
                book_repository = BookAdapter(self.logger_adapter)
                bnf_repository = BnfAdapter(self.logger_adapter)
                open_library_repository = OpenLibraryAdapter(self.logger_adapter)
                service = GetInfosService(
                    [book_repository, bnf_repository, open_library_repository],
                    self.logger_adapter,
                )
            else:
                return self.response_adapter.technical_error("Erreur dans la recherche de profils")

            album = service.main(isbn)

            return self.response_adapter.json(album_to_dict(album))

        except AlbumNotFoundException as e:
            self.logger_adapter.warning(str(e), extra={"isbn": isbn})
            return self.response_adapter.not_found(f"Album {int(isbn)} introuvable")

        except Exception as e:
            self.logger_adapter.error(str(e), extra={"isbn": isbn})
            return self.response_adapter.server_error("Erreur interne")


def album_infos(request: HttpRequest,
                isbn: int) -> HttpResponse | HttpResponseForbidden | HttpResponseNotFound | HttpResponseBadRequest | HttpResponseServerError:
    view = AlbumInfosView()
    return view.handle_request(request, isbn)
