from main.domain.exceptions.api_exceptions import ApiConnexionDataNotFound
from main.infrastructure.api.bd_gest_adapter import BdGestAdapter
from main.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.infrastructure.persistence.database.models import BD
from main.infrastructure.persistence.sheet.sheet_adapter import SheetAdapter

result_isbn = list(BD.objects.values("isbn").filter(synopsis__icontains="Le synopsis de cet album est manquant"))
result_isbn = [album['isbn'] for album in result_isbn]

logging_repository = PythonLoggerAdapter()
adapter = BdGestAdapter(logging_repository)

sheet = SheetAdapter()
sheet.open("bd", "BD")
donnees = sheet.get_all()

j = 19
for isbn in result_isbn:
    try:
        synopsis = adapter.get_infos(isbn).synopsis
    except ApiConnexionDataNotFound as e:
        print("Album inexistant", str(isbn))
    else:

        for i in range(len(donnees)):
            ligne = donnees[i]
            if ligne[0] == str(isbn):
                sheet.set(synopsis, i, j)

