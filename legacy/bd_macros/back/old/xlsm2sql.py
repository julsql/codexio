# Conversion csv en sql

import pandas
from openpyxl import load_workbook

sql = """CREATE TABLE IF NOT EXISTS BD (
	ISBN	BIGINT,
	Album	TEXT,
	Numéro	TEXT,
	Série	TEXT,
	Scénariste	TEXT,
	Dessinateur	TEXT,
	Couleur	TEXT,
	Éditeur	TEXT,
	Date_de_parution	TEXT,
	Édition	TEXT,
	Nombre_de_pages	TEXT,
	Cote	REAL,
	Prix_dachat	REAL,
	Année_dachat	INT,
	Lieu_dachat	TEXT,
	Dédicace	INT,
	Ex_Libris	INT,
	Synopsis	TEXT,
	Image	TEXT
);
INSERT INTO 'BD' ('ISBN', 'Album', 'Numéro', 'Série', 'Scénariste', 'Dessinateur', 'Couleur', 'Éditeur', 'Date_de_parution', 'Édition', 'Nombre_de_pages', 'Cote', 'Prix_dachat', 'Année_dachat', 'Lieu_dachat', 'Dédicace', 'Ex_Libris', 'Synopsis', 'Image') VALUES """

#sql = sql.replace("'", "`")

xlsmFile = "/path/to/bd_database/BD.xlsm"
xlsxFile = "/path/to/bd_database/back/BD.xlsx"
sqlFile = "/path/to/bd_database/back/BD.sql"

# Charger le classeur .xlsm
workbook = load_workbook(xlsmFile, keep_vba=False)

# Enregistrer le classeur sous le format .xlsx sans les macros
workbook.save(xlsxFile)

sheet = pandas.read_excel(xlsxFile, na_values = [0])
sheet = sheet.to_numpy()

def toList(line):
    liste = []
    for value in line:
        liste.append(value)
    return liste

for line in sheet:
    sql += "("
    i = 0
    for info in line[:-1]:
        if i in [0, 13, 15, 16]:
            try:
                info = int(float(info))
            except:
                sql += "NULL, "
            else:
                sql += "{}, ".format(info)

        elif i in [11, 12]:
            try:
                info = float(info)
            except:
                sql += "NULL,"
            else:
                sql += "{}, ".format(info)
        else:
            try:
                info = info.replace("'", "''")
            except:
                None
            finally:
                sql += "'{}', ".format(info)

        i += 1
    sql = sql[:-2]
    sql += "), \n"

sql = sql[:-3]
sql += ";"

sql = sql.replace('nan', 'NULL').replace("'nan'", 'NULL')
sql = sql.replace(" ", "").replace(" ", "").replace("", ". ").replace("œ", "œ")

with open(sqlFile, 'w') as f:
    f.write(sql)
