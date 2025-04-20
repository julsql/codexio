from django.http import HttpRequest

from config.settings import POST_TOKEN
from main.core.common.reponse.utf8_response import UTF8Response, UTF8ResponseNotAllowed, UTF8ResponseForbidden
from main.core.common.sheet.internal.sheet_connexion import SheetConnexion
from main.core.existing_album.existing_album_service import ExistingAlbumService


def existing_album(request: HttpRequest, isbn: int) -> UTF8Response | UTF8ResponseForbidden | UTF8ResponseNotAllowed:
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return UTF8ResponseForbidden("Vous n'avez pas l'autorisation")
        else:
            try:
                sheet_repository = SheetConnexion()
                service = ExistingAlbumService(sheet_repository)
                if service.main(isbn):
                    message = f"Album {isbn} déjà enregistré"
                else:
                    message = f"Album {isbn} jamais enregistré"

                return UTF8Response(message, status=200)
            except Exception as e:
                return UTF8Response(str(e), status=500)
    else:
        return UTF8ResponseNotAllowed(["GET"], "Il faut une requête GET")
