from back.old import InfosBD
from error import Error
from sheet_connection import Conn
import sys
doc_name = "bd"


def liste_from_dict(infos):
    titles = ["ISBN", "Album", "Numéro", "Série", "Scénario", "Dessin", "Couleurs",
              "Éditeur", "Date de publication", "Edition", "Pages", None, "Prix", None, None, None, None, "Synopsis",
              "Image"]

    liste = []
    for title in titles:
        if title in infos:
            liste.append(infos[title])
        elif title is None:
            liste.append("")
        else:
            raise IndexError(f"{title} is missing")
    return liste


def add_line(connection, infos):
    liste = liste_from_dict(infos)
    connection.append(liste)


def add(isbn):
    try:
        connection = Conn()
        connection.open(doc_name)
    except:
        message_log = "Google Sheet non accessible."
        Error(message_log, ISBN)
        return None
    else:
        if connection.double(isbn):
            message_log = f"{ISBN} est déjà dans la base de données"
            Error(message_log, ISBN)
            return None

        infos = InfosBD.main(ISBN)

        if type(infos) is not type(dict()):
            message_log = f"{infos} pas du bon type"
            Error(message_log, ISBN)
            return None

        try:
            add_line(connection, infos)
        except:
            message_log = f"{infos} n'a pas été ajouté correctement"
            Error(message_log, isbn)
            return None
        else:
            print("___C'EST FINI !!___")


if __name__ == "__main__":
    ISBN = sys.argv[1]
    add(ISBN)
