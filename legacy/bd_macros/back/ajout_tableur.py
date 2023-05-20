import InfosBD
import pandas
import openpyxl
import numpy as np
import os
import sys
import time
from datetime import datetime

path = "/path/to/project/"
path = "/path/to/project/"
#path = "/path/to/bd/"
path_back = path + "back/"
fichier_xlsm = path + "BD.xlsm"
fichier_xlsx = path_back + "BD.xlsx"
fichier2 = path_back + "BD_Backup/"
log = path_back + "logs.txt"
ssh = path_back + "path.txt"

ISBN = 9782749301273 # Peter Pan

def xlsx_xlsm():
    # Charger le classeur XLSM
    workbook_xlsm = openpyxl.load_workbook(fichier_xlsm, keep_vba=True)

    # Charger le classeur XLSX
    workbook_xlsx = openpyxl.load_workbook(fichier_xlsx)
    sheet_name = "BD"
    # Copier les valeurs de chaque feuille XLSX vers le classeur XLSM
    worksheet_xlsx = workbook_xlsx[sheet_name]
    worksheet_xlsm = workbook_xlsm[sheet_name]
        
    # Supprimer toutes les lignes existantes dans la feuille worksheet_xlsm
    worksheet_xlsm.delete_rows(1, worksheet_xlsm.max_row)

    # Parcourir les cellules et copier les valeurs
    for row in worksheet_xlsx.iter_rows(values_only=True):
        worksheet_xlsm.append(row)

    # Enregistrer les modifications dans le classeur XLSM
    workbook_xlsm.save(fichier_xlsm)

def deja(ISBN):
    df = pandas.read_excel(fichier_xlsx)
    liste_ISBN = []
    for row in df.itertuples():
        try:
            value = str(int(float(str(row[1]))))
        except ValueError:
            None
        else:
            liste_ISBN.append(value)

    return ISBN in liste_ISBN
    
def addLog(ISBN, message):
    f = open(log, "a")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write("\n" + dt_string + " " +  ISBN + " : " + message)
    f.close()

def backUp():
    try:
        print(fichier_xlsm)
        df = pandas.read_excel(fichier_xlsm)
    except:
        os.chdir(path + 'BD_Backup')
        files = os.listdir()
        files.sort(key=lambda x: os.path.getmtime(x))
        files.reverse()
        print(files)
        for file in files:
            path_file = path_back + "BD_Backup/" + file
            try:
                pandas.read_excel(path_file)
            except:
                None
            else:
                print('rm "{0}"'.format(fichier_xlsm))
                print('cp "{0}" "{1}"'.format(path_file, fichier_xlsm))
                os.popen('rm "{0}"'.format(fichier_xlsm))
                os.popen('cp "{0}" "{1}"'.format(path_file, fichier_xlsm))
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
    
def add_ligne(ISBN, infos):
    # Ouverture du fichier Excel
    wb = openpyxl.load_workbook(fichier_xlsm)

    # Accéder à la feuille de calcul
    ws = wb['BD']

    title = ["Album", "Numéro", "Série", "Scénario", "Dessin", "Couleurs", "Éditeur", "Date de publication", "Edition", "Pages"]

    a = 65
    row = ws.max_row + 1
    my_case = chr(a) + str(row)
    ws[my_case].value = ISBN

    for i in range(len(title)):
        my_case = chr(i + a + 1) + str(row)
        ws[my_case].value = infos[title[i]]

    my_case = "M" + str(row)
    ws[my_case].value = infos["Prix"]

    my_case = "R" + str(row)
    ws[my_case].value = infos["Synopsis"]
    my_case = "S" + str(row)
    ws[my_case].value = infos["Image"]

    # Enregistrer les modifications dans le fichier Excel
    wb.save(fichier_xlsx)


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
        try:
            add_ligne(ISBN, infos)
            xlsx_xlsm()
            print("\n________________________________ C'EST FINI !! ________________________________\n")
        except:
            # Il y a eu une erreur : on restaure BackUp.
            bool = backUp()
            if not bool:
                print("Aucun backup non corrompu disponible")
                addLog(ISBN, "Aucun backup non corrompu disponible")
                print("\n/!\\______________________________ PAS DE BACKUP DISPONIBLE !! ______________________________/!\\\n")
                return None
            
            print('Erreur, on doit restaurer un backup')
            addLog(ISBN, "Restauration backup")
            print("\n/!\\_____________________________ BACKUP TROUVÉ !! _____________________________/!\\\n")
            return None

if __name__ == "__main__":
    #ISBN = sys.argv[1]
    ISBN = "9782864976165"
    with open(ssh, "a") as f:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f.write("\n" + dt_string + " : " +  ISBN)
    # os.popen('mkdir {}'.format(fichier2))
    os.popen('cp "{0}" "{1}BD_{2}.xlsm"'.format(fichier_xlsm, fichier2, ISBN))
    update(ISBN)
