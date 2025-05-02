from main.core.add_album.bd_repository import BdRepository


class BdInMemory(BdRepository):

    def __init__(self, name: str, data: dict) -> None:
        self.name = name
        self.data = data

    def get_infos(self, isbn: int) -> dict:
        return self.data

    def get_url(self, isbn: int) -> str:
        return f"http://mock-{self.name}.com/{isbn}"

    def get_html(self, url: str) -> str:
        return "<html><body><h1>Mock</h1></body></html>"

    def __str__(self) -> str:
        return self.name
