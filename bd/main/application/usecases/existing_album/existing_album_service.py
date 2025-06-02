from main.domain.ports.repositories.sheet_repository import SheetRepository


class ExistingAlbumService:
    def __init__(self, sheet_repository: SheetRepository):
        doc_name = "bd"
        sheet_name = "BD"
        self._sheet_repository = sheet_repository
        self._sheet_repository.open(doc_name, sheet_name)

    def execute(self, isbn: int) -> bool:
        return self._sheet_repository.double(isbn)
