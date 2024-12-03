from bs4 import BeautifulSoup

from main.core.add_album.add_album_error import AddAlbumError
from main.core.update_images.bd_repository import BdRepository


class BdPhileRepository(BdRepository):

    def get_images(self, isbn: int) -> str:
        """Trouver image de BD à partir lien bdphile.fr"""

        url = self.get_url(isbn)
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        meta_tag = soup.find('meta', attrs={'property': 'og:image'})
        if meta_tag:
            image = meta_tag['content']
            return image
        return ""

    def get_url(self, isbn: int) -> str:
        """Trouver lien BD bdphile.fr à partir de son ISBN"""

        search_link = "https://www.bdphile.fr/search/album/?q={}".format(isbn)
        html = self.get_html(search_link)
        soup = BeautifulSoup(html, 'html.parser')
        a_tag = soup.find('a', href=lambda href: href and href.startswith("https://www.bdphile.fr/album/view/"))
        if a_tag:
            return a_tag.get('href')
        else:
            raise AddAlbumError(f"ISBN {isbn} introuvable dans BD Phile")
