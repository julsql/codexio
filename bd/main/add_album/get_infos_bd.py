import re
import urllib.parse
import urllib.request
from main.add_album.error import Error
import datetime
from dateutil import parser
from main.add_album.sheet_connection import Conn
import webbrowser


# Get the data of a comic from its ISBN. Return a dictionary.

def get_link(isbn):
    """Trouver lien BD bdphile.info à partir de son ISBN"""

    search_link = "https://www.bdphile.info/search/album/?q={}".format(isbn)
    web = urllib.request.urlopen(search_link).read().decode('utf-8')

    liste = web.split("\n")
    for ligne in liste:
        if '"https://www.bdphile.info/album/view/' in ligne:
            comic_link = (ligne.split('"')[1])
            return comic_link
    return 0


def get_infos(link, isbn, logs):
    """Trouver infos sur BD à partir lien bdphile.info"""
    web = urllib.request.urlopen(link).read().decode('utf-8')
    liste = web.split("\n")
    info = {}

    n = len(liste)

    i = 0
    i_debut, i_fin = 0, n
    while i < n:
        ligne = liste[i]
        if "https://static.bdphile.info/images/media/cover" in ligne:
            for texte in ligne.split('"'):
                if "Image" not in info and "https://static.bdphile.info/images/media/cover" in texte:
                    info["Image"] = texte
        if "<title>" in ligne:
            titre = re.sub('<[^<>]*>', '', ligne).replace("\t", "").replace(" | Bdphile", "")

        if 'details-section p-lg-b-40 p-lg-t-40' in ligne:
            i_debut = i

        if i_debut > 0 and '</div>' in ligne:
            i_fin = i

        if "Synopsis" in ligne:
            j = 2
            synopsis = ""
            ligne = liste[i + j].strip("</p>").strip("\t")
            while j < 10 and "</div" not in ligne:
                nb = ligne.count("br />")
                synopsis += re.sub('<[^<>]*>', '', ligne) + nb * "<br />"
                j += 1
                ligne = liste[i + j].strip("</p>").strip("\t")

            info["Synopsis"] = synopsis.replace("\'", "'").replace("\r", "").replace(">br />", ">")

        if '<h3 class="p-b-20 p-xs-20 p-xs-b-0">Toutes les <strong>éditions</strong></h3>' in ligne:
            j = 1
            while j < 30:
                ligne = liste[i + j].strip("\t")
                if "Édition " in ligne and "Date de publication" not in info:
                    ligne = re.sub('<[^<>]*>', '', ligne).strip("\t")
                    info["Date de publication"] = " ".join(ligne.split(" ")[-2:])
                j += 1
            i = n

        i += 1

    for i in range(i_debut, i_fin):
        ligne = liste[i].strip("\t")
        if "<h1>" in ligne:
            ligne = liste[i + 1].strip("\t")

            info["Série"] = re.sub('<[^<>]*>', '', ligne).replace("Scénario", "").replace("\t", "")
        if "<h2>" in ligne:
            ligne = re.sub('<[^<>]*>', '', ligne).replace("Scénario", "").replace("\t", "").split(" : ")
            if len(ligne) > 1:
                numero = ligne[0].replace("Tome ", "")
                try:
                    numero = int(numero)
                except ValueError:
                    None
                finally:
                    info["Numéro"] = numero
                info["Album"] = ligne[1]
            else:
                info["Album"] = ligne[0]

        if "Scénario" in ligne:
            info["Scénario"] = re.sub('<[^<>]*>', '', ligne).replace("Scénario", "").replace("\t", "")
        if "Dessin" in ligne:
            info["Dessin"] = re.sub('<[^<>]*>', '', ligne).replace("Dessin", "").replace("\t", "")
        if "Couleurs" in ligne:
            info["Couleurs"] = re.sub('<[^<>]*>', '', ligne).replace("Couleurs", "").replace("\t", "")
        if "Éditeur" in ligne:
            ligne = liste[i + 2].strip("\t")
            info["Éditeur"] = re.sub('<[^<>]*>', '', ligne)
        if "Date de publication" in ligne:
            ligne = liste[i + 1].strip("\t")
            if 'Date de publication' in info:
                if info['Date de publication'] == re.sub('<[^<>]*>', '', ligne):
                    info['Edition'] = "Édition originale"
            else:
                date = re.sub('<[^<>]*>', '', ligne)
                info['Date de publication'] = parse_date(date)

        if "Édition" in ligne:
            if 'Edition' not in info:
                for j in range(1, 4):
                    ligne = liste[i + j].strip("\t")
                    if "Reedition" in ligne:
                        ligne2 = liste[i + j + 1].strip("\t")
                        if "dition" in ligne2:
                            info["Edition"] = re.sub('<[^<>]*>', '', ligne2).split(" - ")[0]
                        else:
                            info["Edition"] = re.sub('<[^<>]*>', '', ligne).split(" - ")[0]
                    else:
                        if "dition" in ligne:
                            info["Edition"] = re.sub('<[^<>]*>', '', ligne).split(" - ")[0]

        if "Format" in ligne:
            ligne = liste[i + 1].strip("\t")
            ligne = re.sub('<[^<>]*>', '', ligne).split(" - ")

            for truc in ligne:
                if "pages" in truc:
                    nb_page = truc.replace(" pages", "")
                    try:
                        info["Pages"] = int(nb_page)
                    except:
                        Error(f"{nb_page} n'est pas un nombre de page correct", isbn, logs)
                        info["Pages"] = nb_page

                if "€" in truc:
                    prix = truc.replace("€", "")
                    try:
                        info["Prix"] = float(prix)
                    except:
                        Error(f"{prix} n'est pas un prix correct", isbn, logs)
                        info["Prix"] = prix

    return info


def corriger_info(info, isbn):
    """Corriger info s'il manque des clefs"""

    keys = ['Série', 'Numéro', 'Album', 'Scénario', 'Dessin', 'Couleurs', 'Éditeur', 'Date de publication', 'Image',
            'Prix', 'Edition', 'Pages', 'Synopsis']

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
        message_log = f"Page inexistante dans la base de données"
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
        int(value)
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
        if condition(my_value):
            isbn = connection.get(i, 0)
            print(f"line: {i + 1}, isbn: {isbn}, value: {my_value}")
            link = get_link("https://www.bdphile.info/search/album/?q={}".format(isbn))
            print(link)
            webbrowser.open(link)
            new_value = input("Nouvelle valeur ")
            connection.set(new_value, i, col_num)
