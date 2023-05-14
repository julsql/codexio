from django.shortcuts import render
from main.forms import RechercheForm
import main.recherche as recherche


# Create your views here.
def home(request):
    infos = recherche.alea()
    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = RechercheForm(request.POST)

        if form.is_valid():
            isbn = request.POST.get('isbn')
            titre = request.POST.get('titre')
            num = request.POST.get('id_numero')
            serie = request.POST.get('id_serie')
            scenariste = request.POST.get('id_scenariste')
            dessinateur = request.POST.get('id_dessinateur')
            editeur = request.POST.get('id_editeur')
            edition = request.POST.get('id_edition')
            annee = request.POST.get('id_annee')
            dedicace = request.POST.get('id_dedicace')
            exlibris = request.POST.get('id_exlibris')
            synopsis = request.POST.get('id_synopsis')

            infos = recherche.recherche_bd(isbn, titre, num, serie, scenariste, dessinateur, editeur, edition, annee,
                                           dedicace, exlibris, synopsis)
            return render(request, 'main/bdrecherche.html', {'form': form, 'infos': infos})
        return render(request, 'main/bdrecherche.html', {'form': form, 'infos': infos})
    # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
    # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).

    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = RechercheForm()

    return render(request, 'main/home.html', {'form': form, 'infos': infos})


def bdrecherche(request):

    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = RechercheForm(request.POST)

        if form.is_valid():
            isbn = request.POST.get('isbn')
            titre = request.POST.get('titre')
            num = request.POST.get('numero')
            serie = request.POST.get('serie')
            scenariste = request.POST.get('scenariste')
            dessinateur = request.POST.get('dessinateur')
            editeur = request.POST.get('editeur')
            edition = request.POST.get('edition')
            annee = request.POST.get('annee')
            dedicace = request.POST.get('dedicace')
            exlibris = request.POST.get('exlibris')
            synopsis = request.POST.get('synopsis')

            infos = recherche.recherche_bd(isbn, titre, num, serie, scenariste, dessinateur, editeur, edition, annee, dedicace, exlibris, synopsis)

            return render(request, 'main/bdrecherche.html', {'form': form, 'infos': infos})
    # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
    # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).

    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = RechercheForm()
    infos = recherche.recherche_bd()
    return render(request, 'main/bdrecherche.html', {'form': form, 'infos': infos})


def dedicace(request):
    dedicaces = recherche.dedicaces()
    exlibris = recherche.exlibris()
    return render(request, 'main/dedicace.html', {'dedicaces': dedicaces, 'exlibris': exlibris})


def pagebd(request, isbn):
    infos = recherche.page(isbn)
    return render(request, 'main/pagebd.html', infos)


def statistiques(request):
    infos = recherche.stat()
    return render(request, 'main/statistiques.html', infos)
