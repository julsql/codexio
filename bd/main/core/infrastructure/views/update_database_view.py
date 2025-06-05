from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, \
    HttpResponseServerError

from config.settings import POST_TOKEN
from main.core.application.usecases.authorization.autorization_service import AuthorizationService
from main.core.application.usecases.request_method.request_method_service import RequestMethodService
from main.core.application.usecases.update_database.update_database_service import UpdateDatabaseService
from main.core.infrastructure.api.bearer_token_adapter import BearerTokenAdapter
from main.core.infrastructure.api.request_method_adapter import RequestMethodAdapter
from main.core.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.core.infrastructure.persistence.database.database_adapter import DatabaseAdapter
from main.core.infrastructure.persistence.sheet.sheet_adapter import SheetAdapter
from main.core.infrastructure.responses.django_response_adapter import DjangoResponseAdapter


class UpdateDatabaseView:
    def __init__(self):
        self.logger_adapter = PythonLoggerAdapter()
        self.response_adapter = DjangoResponseAdapter()
        self.request_method_service = RequestMethodService(RequestMethodAdapter(self.response_adapter))
        self.auth_service = AuthorizationService(
            BearerTokenAdapter(self.response_adapter, POST_TOKEN)
        )

    def handle_request(self,
                       request: HttpRequest) -> HttpResponse | HttpResponseForbidden | HttpResponseNotFound | HttpResponseBadRequest | HttpResponseServerError:

        if method_not_allowed := self.request_method_service.method_not_allowed(request.method, "GET"):
            return method_not_allowed

        if token_invalid := self.auth_service.verify_token(request.headers.get('Authorization')):
            return token_invalid

        try:
            sheet_repository = SheetAdapter()
            database_repository = DatabaseAdapter()
            service = UpdateDatabaseService(sheet_repository, database_repository)
            service.main()
            return self.response_adapter.success('Site web mis à jour correctement')

        except Exception as e:
            self.logger_adapter.error(str(e))
            return self.response_adapter.server_error("Erreur interne")


def update_database(
        request: HttpRequest) -> HttpResponse | HttpResponseForbidden | HttpResponseNotFound | HttpResponseBadRequest | HttpResponseServerError:
    view = UpdateDatabaseView()
    return view.handle_request(request)
