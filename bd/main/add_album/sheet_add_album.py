from main.add_album import get_infos_bd
from main.add_album.error import Error
from main.add_album.sheet_connection import Conn

from main.core.common.logger import logger

def liste_from_dict(infos):
    titles = ["ISBN", "Album", "Numéro", "Série", "Scénario", "Dessin", "Couleurs",
              "Éditeur", "Date de publication", "Édition", "Pages", None, "Prix", None, None, None, None, None, "Synopsis",
              "Image"]

    liste = []
    for title in titles:
        if title in infos:
            liste.append(infos[title])
        elif title is None:
            liste.append("")
        else:
            logger.error(f"{title} manque")
            raise IndexError(f"{title} manque")
    return liste


def add_line(connection, infos):
    liste = liste_from_dict(infos)
    connection.append(liste)


def add(isbn, connection):

    if connection.double(isbn):
        message_log = f"{isbn} est déjà dans la base de données"
        raise Error(message_log, isbn)

    try:
        infos, error = get_infos_bd.main(isbn)
    except Error as e:
        raise Error(str(e), isbn)


    if not isinstance(infos, dict):
        if error is not None:
            raise error
        else:
            message_log = f"{infos} pas du bon type"
            raise Error(message_log, isbn)

    try:
        add_line(connection, infos)
    except:
        message_log = f"{infos} n'a pas été ajouté correctement"
        raise Error(message_log, isbn)
    else:
        if error is not None:
            raise error
        title = infos["Album"]
        if title is None or title == "":
            title = infos["ISBN"]
        logger.info(f"{title} ajouté avec succès !")
        return infos


def add_album(isbn):
    doc_name = "bd"
    sheet_name = "BD"

    if isbn == 0:
        message_log = "Aucun ISBN n'a été renseigné"
        raise Error(message_log, "")
    else:
        try:
            isbn = int(isbn)
        except TypeError:
            if isbn is not None and isbn != "":
                raise Error(f"ISBN {isbn} invalide (doit être un grand entier)", isbn)
            else:
                raise Error("ISBN vide ou nul", isbn)
        else:
            try:
                try:
                    connection = Conn()
                    connection.open(doc_name, sheet_name)
                except:
                    message_log = "Google Sheet non accessible."
                    raise Error(message_log, isbn)
                infos = add(isbn, connection)
            except Error as e:
                return e
            else:
                return infos
