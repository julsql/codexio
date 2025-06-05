from time import sleep

from main.core.infrastructure.persistence.database.models import BD
from main.core.infrastructure.persistence.sheet.sheet_adapter import SheetAdapter

result_isbn = list(BD.objects.values("isbn").filter(edition__icontains="Tirage de tête"))
result_isbn_2 = list(BD.objects.values("isbn").filter(edition__icontains="Tirage de luxe"))
result_isbn = [album['isbn'] for album in result_isbn] + [album['isbn'] for album in result_isbn_2]

print(len(result_isbn))

sheet = SheetAdapter()
sheet.open("bd", "BD")
donnees = sheet.get_all()

count = 0

j = 15
for isbn in result_isbn:
    for i in range(len(donnees)):
        ligne = donnees[i]

        if ligne[0].replace("-", "") == str(isbn) and ("Tirage de tête" in ligne[9] or "Tirage de luxe" in ligne[9]) and \
                ligne[j] != "Oui":
            count += 1
            print(count, isbn)
            sheet.set("Oui", i, j)
    if count % 50 == 49:
        sleep(30)
