from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, \
    HttpResponseServerError

from main.core.application.usecases.authorization.authorization_service import AuthorizationService
from main.core.application.usecases.update_database.update_database_service import UpdateDatabaseService
from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.interface_adapters.bearer_token.bearer_token_adapter import BearerTokenAdapter
from main.core.infrastructure.interface_adapters.profile_type.profile_type_adapter import ProfileTypeAdapter
from main.core.infrastructure.interface_adapters.request_methods.request_method_adapter import RequestMethodAdapter
from main.core.infrastructure.interface_adapters.responses.api_response_adapter import ApiResponseAdapter
from main.core.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.core.infrastructure.persistence.database.models import Collection
from main.core.infrastructure.persistence.database.table_bd_adapter import TableBdAdapter
from main.core.infrastructure.persistence.database.table_book_adapter import TableBookAdapter
from main.core.infrastructure.persistence.sheet.sheet_adapter import SheetAdapter


class UpdateDatabaseView:
    def __init__(self):
        self.logger_adapter = PythonLoggerAdapter()
        self.response_adapter = ApiResponseAdapter()
        self.request_method_adapter = RequestMethodAdapter(self.response_adapter)
        self.profile_type_adapter = ProfileTypeAdapter(self.response_adapter)
        self.auth_service = AuthorizationService(
            BearerTokenAdapter(self.response_adapter)
        )

    def handle_request(self,
                       request: HttpRequest) -> HttpResponse | HttpResponseForbidden | HttpResponseNotFound | HttpResponseBadRequest | HttpResponseServerError:

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

            if profile_type == ProfileType.BD:
                database_repository = TableBdAdapter()
            elif profile_type == ProfileType.BOOK:
                database_repository = TableBookAdapter()
            else:
                return self.response_adapter.technical_error("Erreur dans la recherche de profils")

            service = UpdateDatabaseService(sheet_repository, database_repository)
            service.main(collection)
            return self.response_adapter.success('Site web mis à jour correctement')

        except Exception as e:
            self.logger_adapter.error(str(e))
            return self.response_adapter.server_error(f"{e} Erreur interne")


def update_database(
        request: HttpRequest) -> HttpResponse | HttpResponseForbidden | HttpResponseNotFound | HttpResponseBadRequest | HttpResponseServerError:
    view = UpdateDatabaseView()
    return view.handle_request(request)
