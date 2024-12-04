from django.http import HttpResponse, HttpRequest, JsonResponse
from config.settings import POST_TOKEN
from main.core.add_album.add_album_error import AddAlbumError
from main.core.common.sheet.internal.sheet_connexion import SheetConnexion
from main.core.update_images.internal.bdphile_connexion import BdPhileRepository
from main.core.update_images.update_images_service import UpdateColumnService


def update_images(request: HttpRequest) -> HttpResponse | JsonResponse:
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return HttpResponse("Incorrection token", status=401)
        else:
            try:
                sheet_repository = SheetConnexion()
                bdphile_repository = BdPhileRepository()
                service = UpdateColumnService(bdphile_repository, sheet_repository)
                service.main()
            except AddAlbumError as e:
                return HttpResponse(str(e), status=404)
            except Exception as e:
                return HttpResponse(str(e), status=500)
            else:
                return JsonResponse({'message': 'Colonne des images mise à jour'})
