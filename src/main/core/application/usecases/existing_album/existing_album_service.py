from main.core.domain.ports.repositories.sheet_repository import SheetRepository


class ExistingAlbumService:
    def __init__(self, sheet_repository: SheetRepository):
        self._sheet_repository = sheet_repository
        self._sheet_repository.open()

    def execute(self, isbn: int) -> bool:
        return self._sheet_repository.double(isbn)
