from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseNotFound, HttpResponseForbidden, \
    HttpResponseNotAllowed

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.add_album_service import AddAlbumService
from main.core.add_album.internal.bdfugue_connexion import BdFugueRepository
from main.core.add_album.internal.bdgest_connexion import BdGestRepository
from main.core.add_album.internal.bdphile_connexion import BdPhileRepository
from config.settings import POST_TOKEN
from main.core.common.sheet.internal.sheet_connexion import SheetConnexion


def add_album(request: HttpRequest, isbn: int) -> HttpResponseNotFound | HttpResponseForbidden | HttpResponse:
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return HttpResponseForbidden("Vous n'avez pas l'autorisation")
        else:
            try:
                sheet_repository = SheetConnexion()
                bdfugue_repository = BdFugueRepository()
                bdphile_repository = BdPhileRepository()
                bdgest_repository = BdGestRepository()
                service = AddAlbumService([bdphile_repository, bdgest_repository, bdfugue_repository], sheet_repository)
                service.main(isbn)
            except AddAlbumError as e:
                return HttpResponseNotFound(str(e))
            except Exception as e:
                response = HttpResponse(str(e), status=500)
                response["Content-Type"] = "text/plain; charset=utf-8"
                return response
            else:
                text_response = f'Album {isbn} ajouté avec succès'
                response = HttpResponse(text_response, status=200)
                response["Content-Type"] = "text/plain; charset=utf-8"
                return response
    else:
        return HttpResponseNotAllowed(["GET"], "Il faut une requête GET")
