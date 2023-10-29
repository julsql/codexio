import re
import urllib.parse
import urllib.request

import dateutil
from bs4 import BeautifulSoup
try:
    from main.add_album.error import Error
    from main.add_album.sheet_connection import Conn
except ModuleNotFoundError:
    from error import Error
    from sheet_connection import Conn
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
        print("La requête a échoué. Statut de la réponse :", response.status_code)


def get_link(isbn):
    """Trouver lien BD bdphile.info à partir de son ISBN"""

    search_link = "https://www.bdphile.info/search/album/?q={}".format(isbn)
    html = get_html(search_link)
    soup = BeautifulSoup(html, 'html.parser')
    a_tag = soup.find('a', href=lambda href: href and href.startswith("https://www.bdphile.info/album/view/"))
    if a_tag:
        return a_tag.get('href')
    else:
        return 0


def get_infos(url, isbn, logs):
    """Trouver infos sur BD à partir lien bdphile.info"""

    informations = {}
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    title_tag = soup.find('title')

    if title_tag:
        title_text = title_tag.get_text()
        elements = title_text.split("|")[0].strip()

        elements = elements.split(" - ")
        informations["Album"] = elements[0].strip()
        if len(elements) > 1:
            serie = elements[1].split(".")
            if serie[0] == "One-shot":
                informations["Numéro"] = 1
                informations["Série"] = informations["Album"]
            elif len(serie) > 1:
                informations["Numéro"] = serie[0].strip()
                informations["Série"] = serie[1].strip()
            else:
                informations["Série"] = serie[0].strip()

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
        Error("Problème de date de parution", isbn, logs)
    finally:
        format = informations["Format"]
        del informations["Format"]
        format_list = format.split("-")
        for value in format_list:
            if "pages" in value:
                try:
                    informations["Pages"] = int(value.replace("pages", "").strip())
                except:
                    Error(f"{value} est un nombre de pages incorrect", isbn, logs)

            if "€" in value:
                try:
                    informations["Prix"] = float(value.replace("€", "").strip())
                except:
                    Error(f"{value} est un prix incorrect", isbn, logs)

        meta_tag = soup.find('meta', attrs={'property': 'og:image'})
        if meta_tag:
            informations['Image'] = meta_tag['content']

        synopsis_tag = soup.find('p', class_='synopsis')
        if synopsis_tag:
            cleaned_synopsis = ''.join(str(tag) for tag in synopsis_tag.decode_contents()).strip().replace('\r', '').replace('\n', '').replace('\t', '')
            informations["Synopsis"] = cleaned_synopsis

        # Imprimer les informations extraites
        return informations


def corriger_info(info, isbn):
    """Corriger info s'il manque des clefs"""

    keys = ['Série', 'Numéro', 'Album', 'Scénario', 'Dessin', 'Couleurs', 'Éditeur', 'Date de publication', 'Image',
            'Prix', 'Édition', 'Pages', 'Synopsis']

    for key in keys:
        if key not in info.keys():
            info[key] = ""
    info["ISBN"] = isbn
    return info


def main(isbn, logs):
    """Trouver infos à partir de l'ISBN"""
    try:
        isbn = int(isbn)
    except ValueError:
        if isbn is not None and isbn != "":
            raise Error(f"ISBN {isbn} invalide", isbn, logs)
        else:
            raise Error(f"ISBN vide ou nul", isbn, logs)

    try:
        link = get_link(isbn)
    except ValueError:
        if isbn is not None and isbn != "":
            raise Error(f"ISBN {isbn} invalide", isbn, logs)
        else:
            raise Error(f"ISBN vide ou nul", isbn, logs)

    if link == 0:
        message_log = f"Album inexistant dans la base de données"
        raise Error(message_log, isbn, logs)

    try:
        info = get_infos(link, isbn, logs)
    except (UnicodeDecodeError, ValueError) as e:
        raise Error(str(e), isbn, logs)

    info = corriger_info(info, isbn)

    return info


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
        for date_format in formats:
            try:
                parsed_date = parser.parse(formatted_date, dayfirst=True, fuzzy=True,
                                           default=datetime.datetime(1900, 1, 1))
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                pass

    # Si aucun format de date n'a pu être analysé, renvoyez None ou une valeur par défaut
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
            print(f"line: {i + 1}, isbn: {isbn}, value: {my_value}")
            link = get_link("https://www.bdphile.info/search/album/?q={}".format(isbn))
            print(link)
            webbrowser.open(link)
            new_value = input("Nouvelle valeur ")
            connection.set(new_value, i, col_num)
