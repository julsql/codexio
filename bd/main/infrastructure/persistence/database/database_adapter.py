from main.domain.model.bd import BD as INTERNAL_MODEL_BD
from main.domain.ports.repositories.database_repository import DatabaseRepository

from main.infrastructure.persistence.database.models import BD as DATABASE_MODEL_BD


class DatabaseAdapter(DatabaseRepository):
    def reset_table(self) -> None:
        DATABASE_MODEL_BD.objects.all().delete()

    def insert(self, value: list[INTERNAL_MODEL_BD]) -> None:
        objects = [
            DATABASE_MODEL_BD(
                isbn=row.isbn,
                album=row.title,
                number=row.number,
                series=row.series,
                writer=row.writer,
                illustrator=row.illustrator,
                colorist=row.colorist,
                publisher=row.publisher,
                publication_date=row.publication_date,
                edition=row.edition,
                number_of_pages=row.number_of_pages,
                rating=row.rating,
                purchase_price=row.purchase_price,
                year_of_purchase=row.year_of_purchase,
                place_of_purchase=row.place_of_purchase,
                deluxe_edition=row.deluxe_edition,
                localisation=row.localisation,
                synopsis=row.synopsis,
                image=row.image,
            )
            for row in value
        ]

        DATABASE_MODEL_BD.objects.bulk_create(objects)

    def get_all(self) -> list[dict[str, str]]:
        return list(DATABASE_MODEL_BD.objects.all().values())
