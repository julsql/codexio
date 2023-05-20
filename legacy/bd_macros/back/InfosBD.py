import urllib.request
import urllib.parse
from urllib.parse import quote
import sys, re


def get_link(link):
    "Trouver lien BD bdphile.info à partir ISBN"

    web = urllib.request.urlopen(link).read().decode('utf-8')
    liste = web.split("\n")
    for ligne in liste:
        if '"https://www.bdphile.info/album/view/' in ligne:
            new_link = (ligne.split('"')[1])
            return new_link
    return "pas de lien"

def get_infos(link):
    "Trouver infos sur BD à partir lien bdphile.info"
    web = urllib.request.urlopen(link).read().decode('utf-8')
    liste = web.split("\n")
    info = {}

    n = len(liste)

    i = 0
    i_debut, i_fin = 0, n
    while i < n:
        ligne = liste[i]
        if "https://static.bdphile.info/images/media/cover" in ligne:
            for texte in ligne.split('"'):
                if "Image" not in info and "https://static.bdphile.info/images/media/cover" in texte:
                    info["Image"] = texte
        if "<title>" in ligne:
            titre = re.sub('<[^<>]*>', '', ligne).replace("\t", "").replace(" | Bdphile", "")

        if 'details-section p-lg-b-40 p-lg-t-40' in ligne:
            i_debut = i

        if i_debut > 0 and '</div>' in ligne:
            i_fin = i

        if "Synopsis" in ligne:
            j = 2
            synopsis = ""
            ligne = liste[i+j].strip("</p>").strip("\t")
            while j < 10 and "</div" not in ligne:
                nb = ligne.count("br />")
                synopsis += re.sub('<[^<>]*>', '', ligne) + nb*"<br />"
                j += 1
                ligne = liste[i+j].strip("</p>").strip("\t")

            info["Synopsis"] = synopsis.replace("\'", "'").replace("\r", "").replace(">br />", ">")

        if '<h3 class="p-b-20 p-xs-20 p-xs-b-0">Toutes les <strong>éditions</strong></h3>' in ligne:
            j = 1
            while j<30:
                ligne = liste[i+j].strip("\t")
                if "Édition " in ligne and "Date de publication" not in info:
                    ligne = re.sub('<[^<>]*>', '', ligne).strip("\t")
                    info["Date de publication"] = " ".join(ligne.split(" ")[-2:])
                j += 1
            i = n

        i+=1

    for i in range(i_debut, i_fin):
        ligne = liste[i].strip("\t")
        if "<h1>" in ligne:
            ligne = liste[i+1].strip("\t")

            info["Série"] = re.sub('<[^<>]*>', '', ligne).replace("Scénario", "").replace("\t", "")
        if "<h2>" in ligne:
            ligne = re.sub('<[^<>]*>', '', ligne).replace("Scénario", "").replace("\t", "").split(" : ")
            if len(ligne) > 1:
                info["Numéro"] = ligne[0].replace("Tome ", "")
                info["Album"] = ligne[1]
            else:
                info["Album"] = ligne[0]

        if "Scénario" in ligne:
            info["Scénario"] = re.sub('<[^<>]*>', '', ligne).replace("Scénario", "").replace("\t", "")
        if "Dessin" in ligne:
            info["Dessin"] = re.sub('<[^<>]*>', '', ligne).replace("Dessin", "").replace("\t", "")
        if "Couleurs" in ligne:
            info["Couleurs"] = re.sub('<[^<>]*>', '', ligne).replace("Couleurs", "").replace("\t", "")
        if "Éditeur" in ligne:
            ligne = liste[i+2].strip("\t")
            info["Éditeur"] = re.sub('<[^<>]*>', '', ligne)
        if "Date de publication" in ligne:
            ligne = liste[i+1].strip("\t")
            if 'Date de publication' in info:
                if info['Date de publication'] == re.sub('<[^<>]*>', '', ligne):
                    info['Edition'] = "Édition originale"
            else:
                info['Date de publication'] = re.sub('<[^<>]*>', '', ligne)

        if "Édition" in ligne:
            if 'Edition' not in info:
                for j in range(1, 4):
                    ligne = liste[i+j].strip("\t")
                    if "Reedition" in ligne:
                        ligne2 = liste[i+j+1].strip("\t")
                        if "dition" in ligne2:
                            info["Edition"] = re.sub('<[^<>]*>', '', ligne2).split(" - ")[0]
                        else:
                            info["Edition"] = re.sub('<[^<>]*>', '', ligne).split(" - ")[0]
                    else:
                        if "dition" in ligne:
                            info["Edition"] = re.sub('<[^<>]*>', '', ligne).split(" - ")[0]

        if "Format" in ligne:
            ligne = liste[i+1].strip("\t")
            ligne = re.sub('<[^<>]*>', '', ligne).split(" - ")

            for truc in ligne:
                if "pages" in truc:
                    info["Pages"] = truc.replace(" pages", "")
                if "€" in truc:
                    info["Prix"] = truc.replace("€", "")

    return info

def corriger_info(info):
    "Corriger info s'il manque des clefs"

    keys = ['Série', 'Numéro', 'Album', 'Scénario', 'Dessin', 'Couleurs', 'Éditeur', 'Date de publication', 'Image', 'Prix', 'Edition', 'Pages', 'Synopsis']

    for key in keys:
        if key not in info.keys():
            info[key] = ""
    return info

def main(ISBN):
    "Trouver infos à partir de ISBN"
    link = "https://www.bdphile.info/search/album/?q={}".format(ISBN)
    lien = get_link(link)

    if lien == "pas de lien":
        return "ISBN invalide ou page inexistante dans la base de données"

    try:
        info = get_infos(lien)
    except (UnicodeDecodeError, ValueError) as e:
        return e

    info = corriger_info(info)

    return info


# if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2])

ISBN_p = 9782749301273 # Peter Pan
ISBN_b = 9782205064865 # BlueBerry
ISBN_s = 9782505016748 # Le Scorpion

ISBN_1 = 9782344015773
ISBN_2 = 9782754801096

ISBN_a = 9782203388611

