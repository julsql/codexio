from main.add_album import sheet_add_album
from main.add_album.error import Error
from tests.test_add_album.internal.connection_in_memory import ConnInMemory

def add_album(isbn, doc_name, sheet_name):

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
                connection = ConnInMemory()
                connection.open(doc_name, sheet_name)
            except:
                message_log = "Google Sheet non accessible."
                raise Error(message_log, isbn)
            return sheet_add_album.add(isbn, connection)
