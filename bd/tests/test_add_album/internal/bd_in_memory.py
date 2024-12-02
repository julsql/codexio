from main.core.add_album.bd_repository import BdRepository


class BdInMemory(BdRepository):

    def get_infos(self, isbn: int) -> dict:
        url = self.get_url(isbn)
        html = self.get_html(url)
        return {}

    def get_url(self, isbn: int):
        return f"https://www.bdfugue.com/catalogsearch/result/?q={isbn}"
