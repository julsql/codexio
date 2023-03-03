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
#path = "/path/to/bd/"
path_back = path + "back/"
fichier = path + "BD.xlsm"
fichier_x = path_back + "BD.xlsx"
fichier2 = path + "BD_Backup/"
log = path_back + "logs.txt"
ssh = path_back + "path.txt"

# Ouvrir le fichier Excel .xlsm
wb = xw.Book(fichier)
wb_x = xw.Book(fichier_x)

# Modifier la feuille de calcul
ws = wb.sheets['BD']
ws_x = wb_x.sheets['BD']

# Désactiver les mises à jour de l'écran
app = xw.apps.active
app.screen_updating = False

# Définir le zoom de la feuille à 75%
ws.api.Zoom = 175

# Réactiver les mises à jour de l'écran
app.screen_updating = True

plage_data = ws_x.range('A1:S1').expand('down')

a = 65 # = A

for row in range(plage_data.shape[0]):
    for column in range(plage_data.shape[1]):
        my_case = chr(column + a) + str(row)
        ws.range(my_case).value = ws_x.range(my_case).value

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

"""# Sélectionner la plage de cellules contenant les données
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
ws.range(my_case).value = infos["Image"]"""

# Enregistrer les modifications
wb.save()

# Fermer le fichier Excel
wb.close()