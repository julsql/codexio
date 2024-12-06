from django.db import connections
import random
from django.conf import settings
import os

from config.settings import STATIC_ROOT
from main.core.common.logger.logger import logger


def exec_req_one(req):
    with connections['default'].cursor() as cur:
        cur.execute(req)
        return cur.fetchone()


def page(isbn):
    req = "SELECT ISBN, Album, Numéro, Série, Scénariste, Dessinateur, Couleur, Éditeur, \"Date de parution\", Édition, \"Nombre de page\", Cote, \"Prix d'achat\", \"Année d'achat\", \"Lieu d'achat\", Dédicace, \"Ex Libris\",Synopsis, Image FROM BD WHERE ISBN={};""".format(isbn)
    logger.info(req, extra={"isbn": isbn})
    result = exec_req_one(req)
    infos = {}
    titles = ['ISBN', 'Album', 'Numero', 'Serie', 'Scenariste', 'Dessinateur', 'Couleur', 'Editeur', 'Date_de_parution',
              'Edition', 'Nombre_de_pages', 'Cote', 'Prix_dachat', 'Annee_dachat', 'Lieu_dachat', 'Dedicace',
              'Ex_Libris', 'Synopsis', 'Image']
    for i in range(len(titles)):
        infos[titles[i]] = result[i]
    return infos


def stat():
    nombre = exec_req_one("SELECT count(*) as nombre FROM BD;")[0]
    pages = exec_req_one("SELECT sum(\"Nombre de pages\") as somme FROM BD;")[0]
    dedicaces = exec_req_one("SELECT sum(Dédicace) as dedicaces FROM BD;")[0]
    exlibris = exec_req_one("SELECT sum(\"Ex Libris\") as exlibris FROM BD;")[0]
    prix = exec_req_one("SELECT sum(Cote) as prix FROM BD;")[0]
    tirage = exec_req_one("SELECT count(*) as nombre FROM BD WHERE LOWER(\"Tirage de tête\") = 'oui';")[0]
    infos = {'nombre': int(nombre), 'pages': int(pages),
             'dedicaces': int(dedicaces), 'exlibris': int(exlibris),
             'prix': int(prix), 'tirage': int(tirage)}
    return infos


def count_images_in_directory(directory_path):
    if not os.path.isdir(directory_path):
        return 0

    image_count = 0
    allowed_image_extensions = ".jpeg"  # Ajoutez d'autres extensions d'image au besoin

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension == allowed_image_extensions:
                image_count += 1

    return image_count


def dedicaces():
    image_dir = os.path.join(settings.BASE_DIR, "main/static/main/images/dedicaces")
    infos = []
    dedicaces_sum = 0
    for item in os.listdir(image_dir):
        item_path = os.path.join(image_dir, item)

        # Vérifiez si l'élément est un répertoire
        if os.path.isdir(item_path):
            isbn = item
            nb_dedicace = count_images_in_directory(item_path)
            req = f"SELECT Album, Numéro, Série FROM BD WHERE ISBN = {isbn};"
            result = exec_req_one(req)
            dedicaces_sum += nb_dedicace
            if result is None:
                infos.append({'ISBN': isbn, 'Album': "", 'Numero': "", 'Serie': "",
                              'DedicaceRange': range(1, nb_dedicace + 1), 'Dedicace': nb_dedicace})
            else:

                infos.append({'ISBN': isbn, 'Album': result[0], 'Numero': result[1], 'Serie': result[2],
                              'DedicaceRange': range(1, nb_dedicace + 1), 'Dedicace': nb_dedicace})

    return infos, dedicaces_sum


def exlibris():
    image_dir = os.path.join(settings.BASE_DIR, "main/static/main/images/exlibris")
    infos = []
    exlibris_sum = 0
    for item in os.listdir(image_dir):
        item_path = os.path.join(image_dir, item)

        # Vérifiez si l'élément est un répertoire
        if os.path.isdir(item_path):
            isbn = item
            nb_exlibris = count_images_in_directory(item_path)
            req = f"SELECT Album, Numéro, Série FROM BD WHERE ISBN = {isbn};"
            result = exec_req_one(req)
            exlibris_sum += nb_exlibris
            if result is None:
                infos.append({'ISBN': isbn, 'Album': "", 'Numero': "", 'Serie': "",
                              'ExlibrisRange': range(1, nb_exlibris + 1), 'Exlibris': nb_exlibris})
            else:
                infos.append({'ISBN': isbn, 'Album': result[0], 'Numero': result[1], 'Serie': result[2],
                              'ExlibrisRange': range(1, nb_exlibris + 1), 'Exlibris': nb_exlibris})
    return infos, exlibris_sum


def get_photo_dossier(path):
    if os.path.exists(path) and os.path.isdir(path):
        liste_fichiers = os.listdir(path)

        name = []
        for fichier in liste_fichiers:
            if fichier.endswith(".jpeg"):
                name.append(os.path.basename(fichier))
        return name
    else:
        return []


def exlibris_album(isbn):
    image_dir = os.path.join(STATIC_ROOT, "main/images/exlibris", str(isbn))
    return get_photo_dossier(image_dir)


def dedicaces_album(isbn):
    image_dir = os.path.join(STATIC_ROOT, "main/images/dedicaces", str(isbn))
    return get_photo_dossier(image_dir)
