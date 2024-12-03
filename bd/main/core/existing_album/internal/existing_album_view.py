from django.http import HttpResponse, HttpRequest, JsonResponse
from config.settings import POST_TOKEN
from main.core.common.sheet_connexion import SheetConnexion
from main.core.existing_album.existing_album_service import ExistingAlbumService


def existing_album(request: HttpRequest, isbn: int) -> HttpResponse | JsonResponse:
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return HttpResponse("Incorrection token", status=401)
        else:
            try:
                sheet_repository = SheetConnexion()
                service = ExistingAlbumService(sheet_repository)
                if service.main(isbn):
                    message = f"Album {isbn} déjà enregistré"
                else:
                    message = f"Album {isbn} jamais enregistré"
                return JsonResponse({'message': message}, charset='utf-8')
            except Exception as e:
                return HttpResponse(str(e), status=500)
