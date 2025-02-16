import os

from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from config.settings import POST_TOKEN, MEDIA_ROOT
from main.core.delete_photo.delete_photo_service import DeletePhotoService
from main.core.delete_photo.internal.photo_connexion import PhotoConnexion


@csrf_exempt
def delete_dedicace(request, isbn: int, photo_id: int):
    return delete_photo(request, isbn, photo_id, "dedicaces")

@csrf_exempt
def delete_exlibris(request, isbn: int, photo_id: int):
    return delete_photo(request, isbn, photo_id, "exlibris")

def delete_photo(request, isbn: int, photo_id: int, photo_type: str):
    if request.method == 'DELETE':
        # Vérifier le header Authorization
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return HttpResponseForbidden("Vous n'avez pas l'autorisation")

        # Appeler le service pour supprimer la photo
        dedicace_folder = os.path.join(MEDIA_ROOT, 'main/images/dedicaces')
        exlibris_folder = os.path.join(MEDIA_ROOT, 'main/images/exlibris')
        photo_repository = PhotoConnexion(dedicace_folder, exlibris_folder)
        service = DeletePhotoService(photo_repository)
        if service.main(isbn, photo_id, photo_type):
            return HttpResponse("Photo supprimée correctement", status=200)
        else:
            return HttpResponseNotFound("La photo n'a pas été trouvée")
    else:
        return HttpResponseNotAllowed(["DELETE"], "Il faut une requête DELETE")
