from django.http import HttpRequest

from config.settings import POST_TOKEN
from main.core.common.database.internal.database_connexion import DatabaseConnexion
from main.core.common.reponse.utf8_response import UTF8ResponseNotAllowed, UTF8ResponseForbidden, UTF8Response, \
    UTF8ResponseServerError
from main.core.common.sheet.internal.sheet_connexion import SheetConnexion
from main.core.update_database.update_database_service import UpdateDatabaseService


def update_database(request: HttpRequest) -> UTF8ResponseServerError | UTF8ResponseForbidden | UTF8Response | UTF8ResponseNotAllowed:
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return UTF8ResponseForbidden("Vous n'avez pas l'autorisation")
        else:
            sheet_repository = SheetConnexion()
            database_repository = DatabaseConnexion()
            service = UpdateDatabaseService(sheet_repository, database_repository)
            try:
                service.main()
            except Exception as ex:
                return UTF8ResponseServerError(str(ex))
            text_response = "Site web mis à jour correctement"
            return UTF8Response(text_response, status=200)
    else:
        return UTF8ResponseNotAllowed(["GET"], "Il faut une requête GET")
