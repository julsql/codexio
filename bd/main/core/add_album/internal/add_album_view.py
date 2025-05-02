from django.http import HttpRequest

from config.settings import POST_TOKEN
from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.add_album_service import AddAlbumService
from main.core.add_album.internal.bdgest_connexion import BdGestRepository
from main.core.add_album.internal.bdphile_connexion import BdPhileRepository
from main.core.common.reponse.utf8_response import UTF8Response, UTF8ResponseNotAllowed, UTF8ResponseForbidden, \
    UTF8ResponseNotFound
from main.core.common.sheet.internal.sheet_connexion import SheetConnexion


def add_album(request: HttpRequest,
              isbn: int) -> UTF8Response | UTF8ResponseForbidden | UTF8ResponseNotFound | UTF8ResponseNotAllowed:
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return UTF8ResponseForbidden("Vous n'avez pas l'autorisation")
        else:
            try:
                sheet_repository = SheetConnexion()
                bdphile_repository = BdPhileRepository()
                bdgest_repository = BdGestRepository()
                # bdfugue_repository = BdFugueRepository()
                service = AddAlbumService([bdphile_repository, bdgest_repository], sheet_repository)
                service.main(isbn)
            except AddAlbumError as e:
                return UTF8ResponseNotFound(str(e))
            except Exception as e:
                return UTF8Response(str(e), status=500)
            else:
                text_response = f'Album {isbn} ajouté avec succès'
                return UTF8Response(text_response, status=200)
    else:
        return UTF8ResponseNotAllowed(["GET"], "Il faut une requête GET")
