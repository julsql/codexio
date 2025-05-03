from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt

from config.settings import POST_TOKEN
from main.core.common.reponse.utf8_response import UTF8ResponseForbidden, UTF8Response, UTF8ResponseNotFound, \
    UTF8ResponseNotAllowed
from main.core.delete_photo.delete_photo_service import DeletePhotoService
from main.core.delete_photo.internal.photo_connexion import PhotoConnexion


@csrf_exempt
def delete_dedicace(request: HttpRequest, isbn: int, photo_id: int):
    return delete_photo(request, isbn, photo_id, "dedicaces")


@csrf_exempt
def delete_exlibris(request: HttpRequest, isbn: int, photo_id: int):
    return delete_photo(request, isbn, photo_id, "exlibris")


def delete_photo(request: HttpRequest, isbn: int, photo_id: int,
                 photo_type: str) -> UTF8ResponseForbidden | UTF8Response | UTF8ResponseNotFound | UTF8ResponseNotAllowed:
    if request.method == 'DELETE':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return UTF8ResponseForbidden("Vous n'avez pas l'autorisation")

        # Appeler le service pour supprimer la photo
        photo_repository = PhotoConnexion()
        service = DeletePhotoService(photo_repository)
        if service.main(isbn, photo_id, photo_type):
            return UTF8Response("Photo supprimée correctement", status=200)
        else:
            return UTF8ResponseNotFound("La photo n'a pas été trouvée")
    else:
        return UTF8ResponseNotAllowed(["DELETE"], "Il faut une requête DELETE")
