path = "/path/to/project/"
fichier = path + "BD.xlsm"

import xlwings as xw

infos = {'Image': 'https://static.bdphile.info/images/media/cover/150473.jpg', 'Synopsis': "Franck Sangaré est aux mains des Sax, la famille qui a pris le contrôle de Saint-Elme, et son frère Philippe tarde à répondre aux appels angoissés de madame Dombre. Pendant ce temps, à l'auberge de la Vache Brûlée, Romane Mertens apprend à tirer au pistolet avec Paco tandis que son père passe ses journées à parler seul dans sa chambre... Tout seul, vraiment ?", 'Série': 'Saint-Elme', 'Numéro': '2', 'Album': "L'avenir de la famille", 'Scénario': 'Serge Lehman', 'Dessin': 'Frederik Peeters', 'Éditeur': 'Delcourt', 'Date de publication': '12 janvier 2022', 'Pages': '80', 'Prix': '16.95', 'Couleurs': '', 'Edition': ''}

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

"""# Format
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
        worksheet.write(row_num, 18, infos["Image"], info_format)"""

ws.range('A1').value = 'Hello, World!'
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
print(row)
print(plage_data.shape[1])
# chr(65) == A
a = 65

title = ["ISBN", "Album", "Numéro", "Série", "Scénario", "Dessin", "Couleurs", "Éditeur", "Date de publication", "Edition", "Pages", "Prix", "Synopsis", "Image"]

for i in range(int(plage_data.shape[1])):
    my_case = chr(i + a) + str(row)
    # ws.range('A1').value = infos[tableau[i]]

# Enregistrer les modifications
wb.save()

# Fermer le fichier Excel
wb.close()
