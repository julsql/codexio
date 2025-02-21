from main.core.common.database.internal.bd_model import BD
from main.core.common.database.database_repository import DatabaseRepository


class DatabaseConnexion(DatabaseRepository):
    def create_table(self) -> None:
        BD.objects.all().delete()

    def insert(self, value: list[dict[str, str]]) -> None:
        objects = [
            BD(
                isbn=row["isbn"],
                album=row["album"],
                number=row["number"],
                series=row["series"],
                writer=row["writer"],
                illustrator=row["illustrator"],
                colorist=row["colorist"],
                publisher=row["publisher"],
                publication_date=row["publication_date"],
                edition=row["edition"],
                number_of_pages=row["number_of_pages"],
                rating=row["rating"],
                purchase_price=row["purchase_price"],
                year_of_purchase=row["year_of_purchase"],
                place_of_purchase=row["place_of_purchase"],
                deluxe_edition=row["deluxe_edition"],
                synopsis=row["synopsis"],
                image=row["image"],
            )
            for row in value
        ]

        BD.objects.bulk_create(objects)

    def get_all(self) -> list[dict[str, str]]:
        return list(BD.objects.all().values())
