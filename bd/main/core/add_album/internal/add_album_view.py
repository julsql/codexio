from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseNotFound, HttpResponseForbidden

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.add_album_service import AddAlbumService
from main.core.add_album.internal.bdfugue_connexion import BdFugueRepository
from main.core.add_album.internal.bdphile_connexion import BdPhileRepository
from config.settings import POST_TOKEN
from main.core.common.sheet.internal.sheet_connexion import SheetConnexion


def add_album(request: HttpRequest, isbn: int) -> HttpResponse | JsonResponse:
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return HttpResponseForbidden("Vous n'avez pas l'autorisation")
        else:
            try:
                sheet_repository = SheetConnexion()
                bdfugue_repository = BdFugueRepository()
                bdphile_repository = BdPhileRepository()
                service = AddAlbumService([bdfugue_repository, bdphile_repository], sheet_repository)
                service.main(isbn)
            except AddAlbumError as e:
                return HttpResponseNotFound(str(e))
            except Exception as e:
                return HttpResponse(str(e), status=500)
            else:
                return HttpResponse(f'Album {isbn} ajouté avec succès', status=200)
