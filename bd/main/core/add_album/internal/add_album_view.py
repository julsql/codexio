from django.http import HttpResponse, JsonResponse, HttpRequest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.add_album_service import AddAlbumService
from main.core.add_album.internal.bdfugue_connexion import BdFugueRepository
from main.core.add_album.internal.bdphile_connexion import BdPhileRepository
from config.settings import POST_TOKEN
from main.core.common.sheet_connexion import SheetConnexion


def add_album(request: HttpRequest, isbn: int) -> HttpResponse | JsonResponse:
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return HttpResponse("Incorrection token", status=401)
        else:
            try:
                sheet_repository = SheetConnexion()
                bdfugue_repository = BdFugueRepository()
                bdphile_repository = BdPhileRepository()
                service = AddAlbumService([bdfugue_repository, bdphile_repository], sheet_repository)
                service.main(isbn)
            except AddAlbumError as e:
                return HttpResponse(str(e), status=404)
            except Exception as e:
                return HttpResponse(str(e), status=500)
            else:
                return JsonResponse({'message': f'Album {isbn} ajouté avec succès'})
