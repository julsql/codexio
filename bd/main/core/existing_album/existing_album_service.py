from main.core.common.sheet_repository import SheetRepository


class ExistingAlbumService:
    def __init__(self, sheet_repository: SheetRepository) -> None:
        doc_name = "bd"
        sheet_name = "BD"
        self.connexion = sheet_repository
        self.connexion.open(doc_name, sheet_name)

    def main(self, isbn: int):
        return self.connexion.double(isbn)
