from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseForbidden, \
    HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from main.core.application.usecases.authorization.authorization_service import AuthorizationService
from main.core.application.usecases.upload_photo.upload_photo_service import UploadPhotoService
from main.core.domain.model.attachment_type import AttachmentType
from main.core.infrastructure.interface_adapters.bearer_token.bearer_token_adapter import BearerTokenAdapter
from main.core.infrastructure.interface_adapters.request_methods.request_method_adapter import RequestMethodAdapter
from main.core.infrastructure.interface_adapters.responses.django_response_adapter import DjangoResponseAdapter
from main.core.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.core.infrastructure.persistence.database.models import Collection
from main.core.infrastructure.persistence.file.upload_photo_adapter import UploadPhotoAdapter


class UploadPhotoView:
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
                       photo_type: AttachmentType) -> HttpResponse | HttpResponseForbidden | HttpResponseServerError | HttpResponseBadRequest | HttpResponseNotAllowed:

        if method_not_allowed := self.request_method_adapter.method_not_allowed(request.method, "POST"):
            return method_not_allowed

        collection = self.auth_service.verify_token(request.headers.get('Authorization'))
        if not isinstance(collection, Collection):
            return collection

        try:
            if 'file' in request.FILES:
                uploaded_file = request.FILES['file']
                photo_repository = UploadPhotoAdapter()
                service = UploadPhotoService(photo_repository)
                if service.main(isbn, uploaded_file, photo_type, collection.id):
                    return self.response_adapter.success(f"Photo {isbn} ajoutée avec succès")
                else:
                    return self.response_adapter.bad_request("Le type du fichier est incorrect")

            else:
                return self.response_adapter.bad_request("Aucun fichier n'a été envoyé")

        except Exception as e:
            self.logger_adapter.error(str(e))
            return self.response_adapter.server_error("Erreur interne")


@csrf_exempt
def upload_dedicace_view(request: HttpRequest, isbn: int):
    view = UploadPhotoView()
    return view.handle_request(request, isbn, AttachmentType.SIGNED_COPY)


@csrf_exempt
def upload_exlibris_view(request: HttpRequest, isbn: int):
    view = UploadPhotoView()
    return view.handle_request(request, isbn, AttachmentType.EXLIBRIS)
