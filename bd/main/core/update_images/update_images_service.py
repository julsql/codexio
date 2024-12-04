from main.core.common.logger.logger import logger
from main.core.common.sheet.sheet_repository import SheetRepository
from main.core.update_images.bd_repository import BdRepository


class UpdateColumnService:
    IMAGES_COLUMN = 18

    def __init__(self, bd_repository: BdRepository, sheet_repository: SheetRepository) -> None:
        doc_name = "bd"
        sheet_name = "BD"
        self.repository = bd_repository
        self.connexion = sheet_repository
        self.connexion.open(doc_name, sheet_name)

    def main(self):
        sheet = self.connexion.get_all()
        images = []
        i = 0
        for ligne in sheet[1:]:
            if i % 10 == 0:
                logger.info(f"{i + 1}e album")
            isbn = ligne[0]
            image = ligne[self.IMAGES_COLUMN]
            new_image = self.repository.get_images(isbn)
            if new_image == 0:
                logger.warning(f"L'image pour {isbn} n'a pas été trouvée")
            else:
                image = new_image
            images.append(image)
            i += 1

        self.connexion.set_column(images, self.IMAGES_COLUMN)
