from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden

from config.settings import POST_TOKEN
from main.core.common.database.internal.database_connexion import DatabaseConnexion
from main.core.common.sheet.internal.sheet_connexion import SheetConnexion
from main.core.update_database.update_database_service import UpdateDatabaseService


def update_database(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return HttpResponseForbidden("Vous n'avez pas l'autorisation")
        else:
            sheet_repository = SheetConnexion()
            database_repository = DatabaseConnexion()
            service = UpdateDatabaseService(sheet_repository, database_repository)
            service.main()
            response = HttpResponse("Site web mis à jour correctement", status=200)
            response["Content-Type"] = "text/plain; charset=utf-8"
            return response
    else:
        return HttpResponseNotAllowed(["GET"], "Il faut une requête GET")
