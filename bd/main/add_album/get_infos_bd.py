import re
from main.add_album.logger import logger

from bs4 import BeautifulSoup

from main.add_album.error import Error
from main.add_album.sheet_connection import Conn
import datetime
from dateutil import parser

import webbrowser
import requests


# Get the data of a comic from its ISBN. Return a dictionary.

def get_html(url):
    response = requests.get(url)

    # Vérifiez si la requête a réussi
    if response.status_code == 200:
        return response.text
    else:
        logger.error(f"La requête a échoué. Statut de la réponse : {response.status_code}")


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


def get_infos(url, isbn):
    """Trouver infos sur BD à partir lien bdphile.fr"""

    informations = {}
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    title_tag = soup.find('title')

    if title_tag:
        title_text = title_tag.get_text()
        elements = title_text.split("|")[0].strip()

        elements = elements.split(" - ")
        informations["Série"] = elements[0].strip()
        if len(elements) > 1:
            serie = elements[1].split(".")
            if serie[0] == "One-shot":
                informations["Numéro"] = 1
                informations["Album"] = informations["Série"]
            elif len(serie) > 1:
                informations["Numéro"] = serie[0].strip()
                informations["Album"] = serie[1].strip()
            else:
                informations["Album"] = serie[0].strip()

    keys = ['Scénario', 'Dessin', 'Couleurs', 'Éditeur', 'Date de publication', 'Édition', 'Format']
    current_key = ""
    for tag in soup.find_all(['dt', 'dd']):
        if tag.name == 'dt':
            current_key = tag.get_text(strip=True)
            if current_key in informations.keys():
                current_key = None
        elif tag.name == 'dd':
            if current_key in keys:
                dd_text = " ".join(tag.stripped_strings)
                if current_key in informations.keys():
                    informations[current_key] += "," + dd_text
                else:
                    informations[current_key] = dd_text

    try:
        parsed_date = parser.parse(translate(informations["Date de publication"]),
                                   dayfirst=True, fuzzy=True, default=datetime.datetime(1900, 1, 1))
        informations["Date de publication"] = parsed_date.date().isoformat()
    except:
        Error("Problème de date de parution", isbn)
    finally:
        if "Format" in informations:
            format = informations["Format"]
            del informations["Format"]
            format_list = format.split("-")
            for value in format_list:
                if "pages" in value:
                    try:
                        informations["Pages"] = int(value.replace("pages", "").strip())
                    except:
                        Error(f"{value} est un nombre de pages incorrect", isbn)

                if "€" in value:
                    try:
                        informations["Prix"] = float(value.replace("€", "").strip())
                    except:
                        Error(f"{value} est un prix incorrect", isbn)

        meta_tag = soup.find('meta', attrs={'property': 'og:image'})
        if meta_tag:
            informations['Image'] = meta_tag['content']

        synopsis_tag = soup.find('p', class_='synopsis')
        if synopsis_tag:
            cleaned_synopsis = ''.join(str(tag) for tag in synopsis_tag.decode_contents()).strip().replace('\r',
                                                                                                           '').replace(
                '\n', '').replace('\t', '')
            informations["Synopsis"] = cleaned_synopsis

        logger.info(informations, extra={"isbn": isbn})
        return informations


legende = {"Titre album": "Album", "Tome": "Numéro",
           "Série": "Série", "Scénario": "Scénario",
           "Dessin": "Dessin", "Couleurs": "Couleurs", "Éditeur": "Éditeur",
           "date de parution": "Date de publication", "": "Édition",
           "Nombre de pages": "Pages"}


def get_infos_2(url, isbn):
    """Get infos in BD Fugue"""
    logger.info(url, extra={"isbn": isbn})
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    error_div = soup.find('title', text=re.compile(r'^Résultats de recherche pour :'))
    if error_div:
        raise Error(f"{isbn} n'est pas dans BD Fugue ou il y a ambiguïté", isbn)

    infos = {}

    divs = soup.find_all("div", {"class": ["col label w-1/3 product-attribute-label truncate",
                                           "col data w-2/3 product-attribute-value font-semibold"]})
    for i in range(0, len(divs), 2):
        label = divs[i].text.strip().split(":")[0].strip()
        value = divs[i + 1].text.strip()
        if label == "Auteur(s)":
            personnes = value.split(" , ")
            for personne in personnes:
                match = re.search(r'^([\w\s-]+)\s+\(([^)]+)\)', personne.strip())
                if match:
                    nom = match.group(1)
                    attributs = [attr.strip() for attr in match.group(2).split(',')]
                    for fonction in attributs:
                        if fonction in legende.keys():
                            if fonction in infos:
                                infos[fonction] += "," + nom
                            else:
                                infos[fonction] = nom
        elif label == "Format narratif":
            if value == "Intégrale" or value == "Histoire complète":
                infos["Numéro"] = 1

        elif label in legende.keys():
            if legende[label] == "Pages":
                try:
                    infos[legende[label]] = int(value)
                except:
                    Error("Pas de nombre de page correct trouvé", isbn)
            else:
                infos[legende[label]] = value

    if "Album" not in infos and "Série" in infos:
        infos["Album"] = infos["Série"]

    meta_tag = soup.find("meta", {"property": "product:price:amount"})
    if meta_tag:
        try:
            infos["Prix"] = float(meta_tag.get("content"))
        except:
            meta_tag = soup.find("meta", {"itemprop": "price"})
            if meta_tag:
                try:
                    infos["Prix"] = float(meta_tag.get("content"))
                except:
                    Error("Pas de prix correct trouvé", isbn)
            else:
                Error("Pas de prix correct trouvé", isbn)
    else:
        meta_tag = soup.find("meta", {"itemprop": "price"})
        if meta_tag:
            try:
                infos["Prix"] = float(meta_tag.get("content"))
            except:
                Error("Pas de prix correct trouvé", isbn)
        else:
            Error("Pas de prix correct trouvé", isbn)

    pattern = re.compile(r'https://www\.bdfugue\.com/media/catalog/product/cache/.*')
    image_element = soup.find('img', {'src': pattern})

    if image_element:
        infos["Image"] = image_element.get('src')
    else:
        Error("Pas d'image trouvée", isbn)

    div_tag = soup.find("div", {"itemprop": "description"})

    if div_tag:
        infos["Synopsis"] = div_tag.get_text(strip=True)
    else:
        Error("Pas de synopsis trouvé", isbn)

    return infos


def corriger_info(info, isbn):
    """Corriger info s'il manque des clefs"""

    keys = ['Série', 'Numéro', 'Album', 'Scénario', 'Dessin', 'Couleurs', 'Éditeur', 'Date de publication', 'Image',
            'Prix', 'Édition', 'Pages', 'Synopsis']

    for key in keys:
        if key not in info.keys():
            info[key] = ""
    info["ISBN"] = isbn
    return info


def main(isbn):
    """Trouver infos à partir de l'ISBN"""
    try:
        isbn = int(isbn)
    except ValueError:
        if isbn is None or isbn == "":
            raise Error("ISBN vide ou nul", isbn)
        else:
            raise Error(f"ISBN {isbn} invalide", isbn)
    try:
        link = get_link(isbn)
    except ValueError:
        if isbn is not None and isbn != "":
            raise Error(f"ISBN {isbn} invalide", isbn)
        else:
            raise Error("ISBN vide ou nul", isbn)
    
    if link == 0:
        message_log = "Album inexistant dans BD Phile"
        Error(message_log, isbn)
        try:
            info = get_infos_2(f"https://www.bdfugue.com/catalogsearch/result/?q={isbn}", isbn)
        except Exception:
            info = corriger_info({}, isbn)
            message_log = "Album inexistant dans BD Phile et dans BD Fugue. ISBN ajouté"
            return info, Error(message_log, isbn)

    else:
        try:
            info = get_infos(link, isbn)
        except (UnicodeDecodeError, ValueError) as e:
            raise Error(str(e), isbn)

    info = corriger_info(info, isbn)

    return info, None

TRANSLATED_MONTHS = {
    "janvier": "January",
    "février": "February",
    "fevrier": "February",
    "mars": "March",
    "avril": "April",
    "mai": "May",
    "juin": "June",
    "juillet": "July",
    "août": "August",
    "aout": "August",
    "septembre": "September",
    "octobre": "October",
    "novembre": "November",
    "décembre": "December",
    "decembre": "December",
}


def translate(date_str):
    for mois, month in TRANSLATED_MONTHS.items():
        if mois in date_str.lower():
            date_str = date_str.lower().replace(mois, month)
    return date_str


def parse_date(date_str):
    formatted_date = translate(date_str)

    try:
        # Essayez d'analyser la date directement
        parsed_date = parser.parse(formatted_date, dayfirst=True, fuzzy=True, default=datetime.datetime(1900, 1, 1))

        # Formatez la date analysée en tant qu'objet datetime
        return parsed_date.strftime("%Y-%m-%d")

    except ValueError:
        # Si l'analyse directe échoue, essayez un autre format de date
        formats = [
            "%d %B %Y",
            "%d %b %Y",
            "%B %Y",
            "%b %Y",
            "%d %B %Y",
            "%d %B %Y %H:%M:%S",
            "%d %b %Y %H:%M:%S",
            "%B %Y %H:%M:%S",
            "%b %Y %H:%M:%S",
        ]
        for _ in formats:
            try:
                parsed_date = parser.parse(formatted_date, dayfirst=True, fuzzy=True,
                                           default=datetime.datetime(1900, 1, 1))
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                pass

    return date_str


def condition(value):
    try:
        parser.parse(value, dayfirst=True, fuzzy=True, default=datetime.datetime(1900, 1, 1))
    except:
        return False
    else:
        return True


def corrige_colonne(col_num):
    connection = Conn()
    connection.open("bd")
    value = connection.get_column(col_num)
    for i in range(1, len(value)):
        my_value = value[i]
        if not condition(my_value):
            isbn = connection.get(i, 0)
            logger.info(f"line: {i + 1}, isbn: {isbn}, value: {my_value}", extra={"isbn": isbn})
            link = get_link("https://www.bdphile.fr/search/album/?q={}".format(isbn))
            logger.info(link, extra={"isbn": isbn})
            webbrowser.open(link)
            new_value = input("Nouvelle valeur ")
            connection.set(new_value, i, col_num)
