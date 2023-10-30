from django.db import connections
import random
from django.conf import settings
import os


def exec_req_all(req):
    with connections['default'].cursor() as cur:
        cur.execute(req)
        return cur.fetchall()


def exec_req_one(req):
    with connections['default'].cursor() as cur:
        cur.execute(req)
        return cur.fetchone()


def alea():
    req = "SELECT ISBN, Album, Numéro, Série, Image, Scénariste, Dessinateur, \"Date de parution\", \"Prix d'achat\", " \
          "\"Nombre de pages\", Édition, Synopsis FROM BD ORDER BY RAND() LIMIT 1;"
    result = exec_req_one(req)
    infos = {'ISBN': result[0], 'Album': result[1], 'Numero': result[2], 'Serie': result[3], 'Image': result[4],
             'Scenartiste': result[5], 'Dessinateur': result[6], 'Date_de_parution': result[7],
             'Prix_dachat': result[8], 'Nombre_de_pages': result[9], 'Edition': result[10], 'Synopsis': result[11]}
    return infos


def list_files_in_subdirectories(directory_path):
    # Assurez-vous que le chemin est un répertoire
    if not os.path.isdir(directory_path):
        return []  # Le chemin spécifié n'est pas un répertoire

    files = []
    image_extensions = ['.jpg', '.jpeg', '.png']

    # Parcourez le contenu du répertoire, y compris les sous-répertoires
    for root, dirs, files_in_root in os.walk(directory_path):
        for file_name in files_in_root:

            # Vérifiez si l'extension du fichier est dans la liste des extensions d'image
            if any(file_name.lower().endswith(ext) for ext in image_extensions):
                # Obtenez le nom du répertoire parent et le nom du fichier
                parent_directory = os.path.basename(root)
                grandparent_directory = os.path.basename(os.path.dirname(root))
                # Ajoutez ces informations à la liste
                files.append(os.path.join(grandparent_directory, parent_directory, file_name))

    return files


def banner():
    dedicace_dir = os.path.join(settings.BASE_DIR, "main/static/main/images/dedicaces")
    exlibris_dir = os.path.join(settings.BASE_DIR, "main/static/main/images/exlibris")
    image_files = list_files_in_subdirectories(dedicace_dir) + list_files_in_subdirectories(exlibris_dir)
    if image_files:
        random_image = random.choice(image_files)
        random_image_path = os.path.join(settings.STATIC_URL, "main/images/", random_image)
    else:
        random_image_path = os.path.join(settings.STATIC_URL, "main/images/banner.jpg")
    return random_image_path


def recherche_bd(isbn=None, titre=None, num=None, serie=None, scenariste=None, dessinateur=None, editeur=None,
                 edition=None, annee=None, dedicace=None, exlibris=None, synopsis=None):
    if isbn is None and titre is None and num is None and serie is None and scenariste is None and dessinateur is None and editeur is None and edition is None and annee is None and dedicace is None and exlibris is None and synopsis is None:
        req = "SELECT ISBN, Album, Numéro, Série FROM BD"
    else:
        req = "SELECT ISBN, Album, Numéro, Série FROM BD WHERE"
        if isbn != "":
            req += f" ISBN={isbn} AND"
        if titre != "":
            req += f" Album LIKE '%{titre}%' AND"
        if num != "":
            req += f" Numéro={num} AND"
        if serie != "":
            req += f" Série LIKE '%{serie}%' AND"
        if scenariste != "":
            req += f" Scénariste LIKE '%{scenariste}%' AND"
        if dessinateur != "":
            req += f" Dessinateur LIKE '%{dessinateur}%' AND"
        if editeur != "":
            req += f" Éditeur LIKE '%{editeur}%' AND"
        if edition != "":
            req += f" Édition LIKE '%{edition}%' AND"
        if annee != "":
            req += f" Annee={annee} AND"
        if dedicace != "":
            req += f" Dédicace={dedicace} AND"
        if exlibris != "":
            req += f" \"Ex Libris\"={exlibris} AND"
        if synopsis != "":
            synarray = synopsis.split(" ")
            for i in range(len(synarray)):
                req += f" Synopsis LIKE '%{synarray[i]}%' AND"
        req = req[:-4] + ";"

    result_req = exec_req_all(req)
    infos = []

    for result in result_req:
        infos.append({'ISBN': result[0], 'Album': result[1], 'Numero': result[2], 'Serie': result[3]})
    return infos


def page(isbn):
    req = "SELECT * FROM BD WHERE ISBN={};".format(isbn)
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
    infos = {'nombre': int(nombre), 'pages': int(pages),
             'dedicaces': int(dedicaces), 'exlibris': int(exlibris),
             'prix': int(prix)}
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
    for item in os.listdir(image_dir):
        item_path = os.path.join(image_dir, item)

        # Vérifiez si l'élément est un répertoire
        if os.path.isdir(item_path):
            isbn = item
            nb_dedicace = count_images_in_directory(item_path)
            req = f"SELECT Album, Numéro, Série FROM BD WHERE ISBN = {isbn};"
            result = exec_req_one(req)
            if result is None:
                infos.append({'ISBN': isbn, 'Album': "", 'Numero': "", 'Serie': "",
                              'DedicaceRange': range(1, nb_dedicace + 1), 'Dedicace': nb_dedicace})
            else:

                infos.append({'ISBN': isbn, 'Album': result[0], 'Numero': result[1], 'Serie': result[2],
                              'DedicaceRange': range(1, nb_dedicace + 1), 'Dedicace': nb_dedicace})
    return infos


def exlibris():
    image_dir = os.path.join(settings.BASE_DIR, "main/static/main/images/exlibris")
    infos = []
    for item in os.listdir(image_dir):
        item_path = os.path.join(image_dir, item)

        # Vérifiez si l'élément est un répertoire
        if os.path.isdir(item_path):
            isbn = item
            nb_exlibris = count_images_in_directory(item_path)
            req = f"SELECT Album, Numéro, Série FROM BD WHERE ISBN = {isbn};"
            result = exec_req_one(req)
            if result is None:
                infos.append({'ISBN': isbn, 'Album': "", 'Numero': "", 'Serie': "",
                              'ExlibrisRange': range(1, nb_exlibris + 1), 'Exlibris': nb_exlibris})
            else:
                infos.append({'ISBN': isbn, 'Album': result[0], 'Numero': result[1], 'Serie': result[2],
                              'ExlibrisRange': range(1, nb_exlibris + 1), 'Exlibris': nb_exlibris})
    return infos


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
    image_dir = os.path.join(settings.BASE_DIR, "main/static/main/images/exlibris", str(isbn))
    return get_photo_dossier(image_dir)


def dedicaces_album(isbn):
    image_dir = os.path.join(settings.BASE_DIR, "main/static/main/images/dedicaces", str(isbn))
    return get_photo_dossier(image_dir)
