from django.http import HttpRequest, JsonResponse, HttpResponse

from config.settings import POST_TOKEN
from main.core.common.sheet_connexion import SheetConnexion
from main.core.update_database.update_database_service import UpdateDatabaseService


def update_database(request: HttpRequest) -> HttpResponse | JsonResponse:
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return JsonResponse({'error': "Vous n'avez pas l'autorisation"})
        else:
            sheet_repository = SheetConnexion()
            service = UpdateDatabaseService(sheet_repository)
            service.main()
            return JsonResponse({'message': 'Site web mis à jour correctement'})
    else:
        return JsonResponse({'message': 'Il faut une requête POST'})
