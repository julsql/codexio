import InfosBD
import pandas
import numpy as np
import os
import sys
# from tkinter import messagebox, Tk
from datetime import datetime

path = "/path/to/project/"
path = "/path/to/project/"
path = "/path/to/bd/"
fichier = path + "BD.xlsx"
fichier2 = path + "BD_Backup/"
log = path + "logs.txt"
ssh = path + "path.txt"

ISBN = 9782749301273 # Peter Pan

"""def alert(title, message, kind='info', hidemain=True):
    if kind not in ('error', 'warning', 'info'):
        raise ValueError('Unsupported alert kind.')

    show_method = getattr(messagebox, 'show{}'.format(kind))
    show_method(title, message)"""

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

def erreur():
    # List all files in the home directory
    files = glob.glob(os.path.expanduser(path + "/*"))
    # Sort by modification time (mtime) ascending and descending
    sorted_by_mtime_ascending = sorted(files, key=lambda t: os.stat(t).st_mtime)
    sorted_by_mtime_descending = sorted(files, key=lambda t: -os.stat(t).st_mtime)
    print(sorted_by_mtime_ascending)
    print(sorted_by_mtime_descending)

# Connexion
def update(ISBN):

    try:

        if deja(ISBN):
            message = ISBN + " est déjà dans la base de données"
            addLog(ISBN, message)
            #alert("Doublon", message, kind="warning")
            #raise ValueError(message)
            print("Doublon" + message)
            print("\n________________________________ ERREUR !! ________________________________\n")
            return None

        infos = InfosBD.main(ISBN)

        if type(infos) is not type(dict()):
            addLog(ISBN, infos)
            #alert('Erreur', infos, kind='warning')
            #raise ValueError(infos)
            print('Erreur' + info)
            print("\n/!\\_____________________________ ERREUR !! _____________________________/!\\\n")
            return None
    except:
        addLog(ISBN, "Erreur")
        print('Erreur')
        print("\n/!\\_____________________________ ERREUR !! _____________________________/!\\\n")
        return None
    else:
        try:
            df = pandas.read_excel(fichier)
            writer = pandas.ExcelWriter(fichier, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='BD')
            workbook = writer.book
            worksheet = writer.sheets['BD']
            worksheet.set_zoom(175)

            # Format
            legende_format = workbook.add_format({'bold': False,'text_wrap': False,'align': 'center','color': '#D871E3','border': 0})
            info_format = workbook.add_format({'bold': False,'align': 'left','text_wrap': False, 'border': 0})

            title = ["ISBN", "Album", "Numéro", "Série", "Scénariste", "Dessinateur", "Couleur", "Éditeur", "Date de parution",
                    "Édition", "Nombre de pages", "Cote", "Prix d'achat", "Année d'achat", "Lieu d'achat", "Dédicace", "Ex Libris", "Synopsis", "Image"]

            # Ajout sur chaque case
            for col_num in range(len(title)):
                worksheet.write(0, col_num, title[col_num], legende_format)
            worksheet.write(0, col_num + 1, "", legende_format)

            row_num = 1
            for row in df.itertuples():
                for index in range(len(row) - 1):
                    value = str(row[index + 1])
                    if value == "nan":
                        value = ""
                    worksheet.write(row_num, index, value, info_format)
                worksheet.write(row_num, index+1, "", info_format)
                row_num += 1

            for index in range(14):
                if index == 0:
                    worksheet.write(row_num, index, ISBN, info_format)
                elif index == 1:
                    worksheet.write(row_num, index, infos["Album"], info_format)
                elif index == 2:
                    worksheet.write(row_num, index, infos["Numéro"], info_format)
                elif index == 3:
                    worksheet.write(row_num, index, infos["Série"], info_format)
                elif index == 4:
                    worksheet.write(row_num, index, infos["Scénario"], info_format)
                elif index == 5:
                    worksheet.write(row_num, index, infos["Dessin"], info_format)
                elif index == 6:
                    worksheet.write(row_num, index, infos["Couleurs"], info_format)
                elif index == 7:
                    worksheet.write(row_num, index, infos["Éditeur"], info_format)
                elif index == 8:
                    worksheet.write(row_num, index, infos["Date de publication"], info_format)
                elif index == 9:
                    worksheet.write(row_num, index, infos["Edition"], info_format)
                elif index == 10:
                    worksheet.write(row_num, index, infos["Pages"], info_format)
                elif index == 11:
                    worksheet.write(row_num, index+1, infos["Prix"], info_format)
                elif index == 12:
                    worksheet.write(row_num, 17, infos["Synopsis"], info_format)
                elif index == 13:
                    worksheet.write(row_num, 18, infos["Image"], info_format)

            writer.save()
            print("\n________________________________ C'EST FINI !! ________________________________\n")
        except:
            # Il y a eu une erreur : on restaure BackUp.

            



            print('Erreur' + info)
            print("\n/!\\_____________________________ ERREUR !! _____________________________/!\\\n")




            return None


if __name__ == "__main__":
    ISBN = sys.argv[1]
    fichier = open(ssh, "a")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    fichier.write("\n" + dt_string + " : " +  ISBN)
    fichier.close()
    os.popen('mkdir {}'.format(fichier2))
    os.popen('cp "{0}" "{1}BD_{2}.xlsx"'.format(fichier, fichier2, ISBN))
    update(ISBN)
