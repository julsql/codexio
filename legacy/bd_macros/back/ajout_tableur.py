import InfosBD
import pandas
import xlwings as xw
import numpy as np
import os
import sys
import time
from datetime import datetime

path = "/path/to/project/"
path = "/path/to/project/"
path = "/path/to/bd/"
path_back = path + "back/"
fichier = path + "BD.xlsm"
fichier2 = path + "BD_Backup/"
log = path_back + "logs.txt"
ssh = path_back + "path.txt"

ISBN = 9782749301273 # Peter Pan

def deja(ISBN):
    df = pandas.read_excel(fichier)
    liste_ISBN = []
    for row in df.itertuples():
        value = str(int(float(str(row[1]))))
        liste_ISBN.append(value)

    return ISBN in liste_ISBN
    
def addLog(ISBN, message):
    fichier = open(log, "a")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    fichier.write("\n" + dt_string + " " +  ISBN + " : " + message)
    fichier.close()

def backUp():
    try:
        print(fichier)
        df = pandas.read_excel(fichier)
    except:
        os.chdir(path + 'BD_Backup')
        files = os.listdir()
        files.sort(key=lambda x: os.path.getmtime(x))
        files.reverse()
        print(files)
        for file in files:
            path_file = path + "BD_Backup/" + file
            try:
                df = pandas.read_excel(path_file)
            except:
                None
            else:
                print('rm "{0}"'.format(fichier))
                print('cp "{0}" "{1}"'.format(path_file, fichier))
                os.popen('rm "{0}"'.format(fichier))
                os.popen('cp "{0}" "{1}"'.format(path_file, fichier))
                time.sleep(1)
                return True
        message = "La copie n'a pas pu être effectué, aucun fichier non corrompu n'est disponible dans les backups"
        addLog("", message)
        print(message)
        print("\n/!\\_____________________________ PAS DE FICHIER NON CORROMPU DE TROUVÉ !! _____________________________/!\\\n")
        return False
    else:
        print("Le fichier BD.xlsx n'est pas corrompu")
        return True

# Connexion
def update(ISBN, loop = 0):

    try:

        if deja(ISBN):
            message = ISBN + " est déjà dans la base de données"
            addLog(ISBN, message)
            print("Doublon " + message)
            print("\n________________________________ ERREUR !! ________________________________\n")
            return None

        infos = InfosBD.main(ISBN)

        if type(infos) is not type(dict()):
            addLog(ISBN, infos)
            print('Erreur ', end="")
            print(infos)
            print("\n/!\\_____________________________ ERREUR !! _____________________________/!\\\n")
            return None
    except:
        addLog(ISBN, "On tente un backup")
        bool = backUp()
        if not bool:
            print("Aucun backup non corrompu disponible")
            addLog(ISBN, "Aucun backup non corrompu disponible")
            print("\n/!\\______________________________ PAS DE BACKUP DISPONIBLE !! ______________________________/!\\\n")
        if loop > 0:
            print('Problème avec le livre, même en cherchant un backup')
            addLog(ISBN, "Problème avec le livre, même en cherchant un backup et en retantant.")
            print("\n/!\\______________________________ PROBLÈME DE LIVRE !! ______________________________/!\\\n")
            return None
        else:
            addLog(ISBN, "On retente une fois")
            print("On retente une fois")
            update(ISBN, 1)
    else:
        #try:
        # Créer l'objet JSON contenant le nom du fichier
        json_obj = {'path': fichier}

        # Ouvrir le fichier Excel en utilisant l'objet JSON
        wb = xw.Book(json=json_obj)
        # Ouvrir le fichier Excel .xlsm
        wb = xw.Book(fichier)

        # Modifier la feuille de calcul
        ws = wb.sheets['BD']

        # Désactiver les mises à jour de l'écran
        app = xw.apps.active
        app.screen_updating = False

        # Définir le zoom de la feuille à 75%
        ws.api.Zoom = 175

        # Réactiver les mises à jour de l'écran
        app.screen_updating = True

        # Colors
        plage = ws.range('A1:S1')

        plage.api.Style = 'Normal'
        plage.font.color = (216, 113, 227)
        plage.horizontal_alignment = 'center'
        plage.font.bold = True

        plage = ws.range('A2:S2').expand('down')

        plage.api.Style = 'Normal'
        plage.font.color = (0, 0, 0)
        plage.horizontal_alignment = 'left'
        plage.font.bold = False

        # Sélectionner la plage de cellules contenant les données
        plage_data = ws.range('A1:S1').expand('down')

        # Parcourir chaque ligne à partir de la fin pour trouver la dernière ligne non vide
        row = plage_data.shape[0]+1
        a = 65 # = A

        title = ["Album", "Numéro", "Série", "Scénario", "Dessin", "Couleurs", "Éditeur", "Date de publication", "Edition", "Pages"]
        
        my_case = chr(a) + str(row)
        ws.range(my_case).value = ISBN

        for i in range(len(title)):
            my_case = chr(i + a + 1) + str(row)
            ws.range(my_case).value = infos[title[i]]

        my_case = "M" + str(row)
        ws.range(my_case).value = infos["Prix"]

        my_case = "R" + str(row)
        ws.range(my_case).value = infos["Synopsis"]
        my_case = "S" + str(row)
        ws.range(my_case).value = infos["Image"]

        # Enregistrer les modifications
        wb.save()

        # Fermer le fichier Excel
        wb.close()
        print("\n________________________________ C'EST FINI !! ________________________________\n")
        #except:
            # Il y a eu une erreur : on restaure BackUp.
        """bool = backUp()
        if not bool:
            print("Aucun backup non corrompu disponible")
            addLog(ISBN, "Aucun backup non corrompu disponible")
            print("\n/!\\______________________________ PAS DE BACKUP DISPONIBLE !! ______________________________/!\\\n")
            return None
        
        print('Erreur, on doit restaurer un backup')
        addLog(ISBN, "Restauration backup")
        print("\n/!\\_____________________________ BACKUP TROUVÉ !! _____________________________/!\\\n")
        return None"""

if __name__ == "__main__":
    ISBN = sys.argv[1]
    with open(ssh, "a") as f:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f.write("\n" + dt_string + " : " +  ISBN)
    # os.popen('mkdir {}'.format(fichier2))
    os.popen('cp "{0}" "{1}BD_{2}.xlsm"'.format(fichier, fichier2, ISBN))
    update(ISBN)
