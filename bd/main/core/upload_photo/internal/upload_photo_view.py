import os
from config.settings import MEDIA_ROOT

from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from config.settings import POST_TOKEN
from main.core.upload_photo.internal.photo_connexion import PhotoConnexion
from main.core.upload_photo.upload_photo_service import UploadPhotoService


@csrf_exempt
def upload_dedicace(request, isbn: int):
    return upload_photo(request, isbn, "dedicaces")

@csrf_exempt
def upload_exlibris(request, isbn: int):
    return upload_photo(request, isbn, "exlibris")

def upload_photo(request: HttpRequest, isbn: int, photo_type: str) -> HttpResponse:
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return HttpResponseForbidden("Vous n'avez pas l'autorisation")
        else:
            if 'file' in request.FILES:
                uploaded_file = request.FILES['file']
                dedicace_folder = os.path.join(MEDIA_ROOT, 'main/images/dedicaces')
                exlibris_folder = os.path.join(MEDIA_ROOT, 'main/images/exlibris')
                photo_repository = PhotoConnexion(dedicace_folder, exlibris_folder)
                service = UploadPhotoService(photo_repository)
                if service.main(isbn, uploaded_file, photo_type):
                    return HttpResponse(
                        f"Photo {isbn} ajoutée avec succès",
                        status=200
                    )
                else:
                    return HttpResponseBadRequest("Le type du fichier est incorrect")
            else:
                return HttpResponseBadRequest("Aucun fichier n'a été envoyé")
    else:
        return HttpResponseNotAllowed(["POST"], "Il faut une requête POST")
