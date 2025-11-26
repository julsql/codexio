from django import forms


class RechercheBookForm(forms.Form):
    title = forms.CharField(required=False, label='Titre', widget=forms.TextInput(attrs={"data_see": "true"}))
    writer = forms.CharField(required=False, label='Écrivain', widget=forms.TextInput(attrs={"data_see": "true"}))
    collection_book = forms.CharField(required=False, label='Collection',
                                  widget=forms.TextInput(attrs={"data_see": "true"}))
    publisher = forms.CharField(required=False, label='Éditeur', widget=forms.TextInput(attrs={"data_see": "true"}))
    start_date = forms.DateField(required=False, label='Date de parution',
                                 widget=forms.DateInput(attrs={"type": "date", "data_see": "true"}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date", "data_see": "true"}))

    # Voir plus
    year_of_purchase = forms.IntegerField(required=False, label="Année d'achat",
                                          widget=forms.NumberInput(attrs={"data_see": "false"}))
    edition = forms.CharField(required=False, label='Édition', widget=forms.TextInput(attrs={"data_see": "false"}))
    literary_genre = forms.CharField(required=False, label='Genre littéraire', widget=forms.TextInput(attrs={"data_see": "false"}))
    style = forms.CharField(required=False, label='Style', widget=forms.TextInput(attrs={"data_see": "false"}))
    origin_language = forms.CharField(required=False, label="Langue d'écriture", widget=forms.TextInput(attrs={"data_see": "false"}))
    isbn = forms.IntegerField(required=False, label='ISBN', widget=forms.NumberInput(attrs={"data_see": "false"}))
    number = forms.CharField(required=False, label='Numéro', widget=forms.TextInput(attrs={"data_see": "false"}))
    synopsis = forms.CharField(required=False, label='Synopsis', widget=forms.TextInput(attrs={"data_see": "false"}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nom d\'utilisateur')
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')

class EmailUpdateForm(forms.Form):
    email = forms.EmailField(label="Nouvel email", max_length=254)
