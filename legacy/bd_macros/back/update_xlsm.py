import xlwings as xw

path = "/path/to/project/"
path = "/path/to/project/"
#path = "/path/to/bd/"
path_back = path + "back/"
fichier = path + "BD.xlsm"
fichier_x = path_back + "BD.xlsx"

# Ouvrir le fichier Excel .xlsm
wb = xw.Book(fichier)
wb_x = xw.Book(fichier_x)
# Modifier la feuille de calcul
ws = wb.sheets['BD']
ws_x = wb_x.sheets['BD']
# Désactiver les mises à jour de l'écran
#app = xw.apps.active
#app.screen_updating = False
# Définir le zoom de la feuille à 175%
#ws.api.Zoom = 175

# Réactiver les mises à jour de l'écran

ws_x.range('A1').expand('table').copy(destination=ws.range('A1'))
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

# Enregistrer les modifications
#app.screen_updating = True
wb.save()

# Fermer le fichier Excel
wb.close()

print("OKÉ")