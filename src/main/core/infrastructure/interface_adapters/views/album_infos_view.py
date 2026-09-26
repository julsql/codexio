from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, \
    HttpResponseServerError

from config.settings import ALBUM_CACHE_TTL_DAYS
from main.core.application.usecases.add_album.get_infos_service import GetInfosService
from main.core.application.usecases.authorization.authorization_service import AuthorizationService
from main.core.domain.exceptions.album_exceptions import AlbumNotFoundException, \
    AlbumSourcesUnavailableException
from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.api.album_repositories_factory import available_sources, build_album_repositories
from main.core.infrastructure.interface_adapters.bearer_token.bearer_token_adapter import BearerTokenAdapter
from main.core.infrastructure.interface_adapters.profile_type.profile_type_adapter import ProfileTypeAdapter
from main.core.infrastructure.interface_adapters.request_methods.request_method_adapter import RequestMethodAdapter
from main.core.infrastructure.interface_adapters.responses.api_response_adapter import ApiResponseAdapter
from main.core.infrastructure.interface_adapters.views.formatters import album_to_dict
from main.core.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.core.infrastructure.persistence.database.album_cache_adapter import AlbumCacheAdapter
from main.core.infrastructure.persistence.database.models import Collection


class AlbumInfosView:
    def __init__(self):
        self.logger_adapter = PythonLoggerAdapter()
        self.cache_adapter = AlbumCacheAdapter(self.logger_adapter, ALBUM_CACHE_TTL_DAYS)
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

            source = request.GET.get('source')
            repositories = build_album_repositories(profile_type, self.logger_adapter, source,
                                                   self.cache_adapter)
            if not repositories:
                if source is not None:
                    return self.response_adapter.bad_request(
                        "Source inconnue, sources disponibles : "
                        + ", ".join(available_sources(profile_type))
                    )
                return self.response_adapter.technical_error("Erreur dans la recherche de profils")

            service = GetInfosService(repositories, self.logger_adapter)
            album = service.main(isbn)

            return self.response_adapter.json(album_to_dict(album))

        except AlbumSourcesUnavailableException as e:
            self.logger_adapter.error(str(e), isbn=isbn)
            return self.response_adapter.technical_error(
                "Sources indisponibles : " + ", ".join(e.sources)
            )

        except AlbumNotFoundException as e:
            self.logger_adapter.warning(str(e), isbn=isbn)
            return self.response_adapter.not_found(f"Album {int(isbn)} introuvable")

        except Exception as e:
            self.logger_adapter.error(str(e), isbn=isbn)
            return self.response_adapter.server_error("Erreur interne")


def album_infos(request: HttpRequest,
                isbn: int) -> HttpResponse | HttpResponseForbidden | HttpResponseNotFound | HttpResponseBadRequest | HttpResponseServerError:
    view = AlbumInfosView()
    return view.handle_request(request, isbn)
