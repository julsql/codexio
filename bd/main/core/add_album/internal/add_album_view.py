from django.http import HttpResponse, JsonResponse, HttpRequest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.add_album_service import AddAlbumService
from main.core.add_album.internal.bdfugue_connexion import BdFugueRepository
from main.core.add_album.internal.bdphile_connexion import BdPhileRepository
from main.core.common.api import POST_TOKEN
from main.core.common.gsheet_connexion import GsheetConnexion


def add_album(request: HttpRequest, isbn: int):
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return HttpResponse("Incorrection token", status=401)
        else:
            try:
                gsheet_repository = GsheetConnexion()
                bdfugue_repository = BdFugueRepository()
                bdphile_repository = BdPhileRepository()
                service = AddAlbumService(isbn, [bdfugue_repository, bdphile_repository], gsheet_repository)
                service.main()
            except AddAlbumError as e:
                return HttpResponse(str(e), status=404)
            except Exception as e:
                return HttpResponse(str(e), status=500)
            else:
                return JsonResponse({'message': f'Album {isbn} ajouté avec succès'})
