from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, \
    HttpResponseServerError

from config.settings import POST_TOKEN
from main.application.usecases.authorization.autorization_service import AuthorizationService
from main.application.usecases.request_method.request_method_service import RequestMethodService
from main.application.usecases.update_database.update_database_service import UpdateDatabaseService
from main.infrastructure.api.bearer_token_adapter import BearerTokenAdapter
from main.infrastructure.api.request_method_adapter import RequestMethodAdapter
from main.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.infrastructure.persistence.database.database_adapter import DatabaseAdapter
from main.infrastructure.persistence.sheet.sheet_adapter import SheetAdapter
from main.infrastructure.responses.django_response_adapter import DjangoResponseAdapter


class UpdateDatabaseView:
    def __init__(self):
        self.auth_service = AuthorizationService(
            BearerTokenAdapter(POST_TOKEN)
        )
        self.request_method_service = RequestMethodService(RequestMethodAdapter())
        self.logger_adapter = PythonLoggerAdapter()
        self.response_adapter = DjangoResponseAdapter()

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
