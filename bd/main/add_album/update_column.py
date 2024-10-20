from bs4 import BeautifulSoup
import requests

from error import Error
from sheet_connection import Conn


def get_html(url):
    response = requests.get(url)

    # Vérifiez si la requête a réussi
    if response.status_code == 200:
        return response.text
    else:
        print("La requête a échoué. Statut de la réponse :", response.status_code)


def get_link(isbn):
    """Trouver lien BD bdphile.fr à partir de son ISBN"""

    search_link = "https://www.bdphile.fr/search/album/?q={}".format(isbn)
    html = get_html(search_link)
    soup = BeautifulSoup(html, 'html.parser')
    a_tag = soup.find('a', href=lambda href: href and href.startswith("https://www.bdphile.fr/album/view/"))
    if a_tag:
        return a_tag.get('href')
    else:
        return 0


def get_image(url):
    """Trouver image de BD à partir lien bdphile.fr"""

    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    meta_tag = soup.find('meta', attrs={'property': 'og:image'})
    if meta_tag:
        image = meta_tag['content']
        return image
    return 0


def update_column(column, logs="logs.txt"):
    try:
        connection = Conn(logs)
        connection.open("bd", "BD")
    except:
        message_log = "Google Sheet non accessible."
        raise Error(message_log, 0, logs)
    else:
        sheet = connection.get_all()
        images = []
        i = 0
        for ligne in sheet[1:]:
            if i % 10 == 0:
                print(f"{i + 1}e album")
            isbn = ligne[0]
            url = get_link(isbn)
            image = ligne[column]
            if url == 0:
                print("Album non trouvé")
            else:
                new_image = get_image(url)
                if new_image == 0:
                    print(f"L'image pour {isbn} n'a pas été trouvée")
                else:
                    image = new_image
            images.append(image)
            i += 1

        connection.set_column(images, column)


update_column(18)
