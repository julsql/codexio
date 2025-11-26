from main.core.domain.model.bd import BD as INTERNAL_MODEL_BD
from main.core.domain.ports.repositories.table_bd_repository import DatabaseRepository
from main.core.infrastructure.persistence.database.models import Collection
from main.core.infrastructure.persistence.database.models.bd import BD as DATABASE_MODEL_BD


class TableBdAdapter(DatabaseRepository):
    def reset_table(self, collection_id: int) -> None:
        DATABASE_MODEL_BD.objects.filter(collection=collection_id).delete()

    def insert(self, value: list[INTERNAL_MODEL_BD], collection: Collection) -> None:
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
                collection=collection,
            )
            for row in value
        ]

        DATABASE_MODEL_BD.objects.bulk_create(objects)

    def get_all(self, collection_id: int) -> list[dict[str, str]]:
        return list(DATABASE_MODEL_BD.objects.filter(collection=collection_id).values())
