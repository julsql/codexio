from django.http import HttpRequest, HttpResponseNotFound, HttpResponseServerError, HttpResponseNotAllowed, \
    HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from main.core.application.usecases.authorization.authorization_service import AuthorizationService
from main.core.application.usecases.delete_photo.delete_photo_service import DeletePhotoService
from main.core.domain.model.attachment_type import AttachmentType
from main.core.infrastructure.interface_adapters.bearer_token.bearer_token_adapter import BearerTokenAdapter
from main.core.infrastructure.interface_adapters.request_methods.request_method_adapter import RequestMethodAdapter
from main.core.infrastructure.interface_adapters.responses.django_response_adapter import DjangoResponseAdapter
from main.core.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.core.infrastructure.persistence.database.models import Collection
from main.core.infrastructure.persistence.file.delete_photo_adapter import DeleteDeletePhotoAdapter


class DeletePhotoView:
    def __init__(self):
        self.logger_adapter = PythonLoggerAdapter()
        self.response_adapter = DjangoResponseAdapter()
        self.request_method_adapter = RequestMethodAdapter(self.response_adapter)
        self.auth_service = AuthorizationService(
            BearerTokenAdapter(self.response_adapter)
        )

    def handle_request(self,
                       request: HttpRequest,
                       isbn: int,
                       photo_id: int,
                       photo_type: AttachmentType) -> HttpResponse | HttpResponseForbidden | HttpResponseServerError | HttpResponseNotFound | HttpResponseNotAllowed:

        if method_not_allowed := self.request_method_adapter.method_not_allowed(request.method, "DELETE"):
            return method_not_allowed

        collection = self.auth_service.verify_token(request.headers.get('Authorization'))
        if not isinstance(collection, Collection):
            return collection

        try:
            photo_repository = DeleteDeletePhotoAdapter()
            service = DeletePhotoService(photo_repository)
            if service.main(isbn, photo_id, photo_type, collection.id):
                return self.response_adapter.success("Photo supprimée correctement")
            else:
                return self.response_adapter.not_found("La photo n'a pas été trouvée")

        except Exception as e:
            self.logger_adapter.error(str(e))
            return self.response_adapter.server_error("Erreur interne")


@csrf_exempt
def delete_dedicace(request: HttpRequest, isbn: int, photo_id: int):
    view = DeletePhotoView()
    return view.handle_request(request, isbn, photo_id, AttachmentType.SIGNED_COPY)


@csrf_exempt
def delete_exlibris(request: HttpRequest, isbn: int, photo_id: int):
    view = DeletePhotoView()
    return view.handle_request(request, isbn, photo_id, AttachmentType.EXLIBRIS)
