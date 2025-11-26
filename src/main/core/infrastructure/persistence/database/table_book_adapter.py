from main.core.domain.model.book import Book as INTERNAL_MODEL_BOOK
from main.core.domain.ports.repositories.table_bd_repository import DatabaseRepository
from main.core.infrastructure.persistence.database.models import Collection
from main.core.infrastructure.persistence.database.models.book import Book as DATABASE_MODEL_BOOK


class TableBookAdapter(DatabaseRepository):
    def reset_table(self, collection_id: int) -> None:
        DATABASE_MODEL_BOOK.objects.filter(collection=collection_id).delete()

    def insert(self, value: list[INTERNAL_MODEL_BOOK], collection: Collection) -> None:
        objects = [
            DATABASE_MODEL_BOOK(
                isbn=row.isbn,
                title=row.title,
                writer=row.writer,
                translator=row.translator,
                publisher=row.publisher,
                collection_book=row.collection_book,
                publication_date=row.publication_date,
                edition=row.edition,
                number_of_pages=row.number_of_pages,
                literary_genre=row.literary_genre,
                style=row.style,
                origin_language=row.origin_language,
                purchase_price=row.purchase_price,
                year_of_purchase=row.year_of_purchase,
                place_of_purchase=row.place_of_purchase,
                localisation=row.localisation,
                synopsis=row.synopsis,
                image=row.image,
                collection=collection,
            )
            for row in value
        ]

        DATABASE_MODEL_BOOK.objects.bulk_create(objects)

    def get_all(self, collection_id: int) -> list[dict[str, str]]:
        return list(DATABASE_MODEL_BOOK.objects.filter(collection=collection_id).values())
