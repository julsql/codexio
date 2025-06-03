from django import forms


class RechercheForm(forms.Form):
    series = forms.CharField(required=False, label='Série', widget=forms.TextInput(attrs={"data_see": "true"}))
    album = forms.CharField(required=False, label='Album', widget=forms.TextInput(attrs={"data_see": "true"}))
    writer = forms.CharField(required=False, label='Scénariste', widget=forms.TextInput(attrs={"data_see": "true"}))
    illustrator = forms.CharField(required=False, label='Dessinateur',
                                  widget=forms.TextInput(attrs={"data_see": "true"}))
    publisher = forms.CharField(required=False, label='Éditeur', widget=forms.TextInput(attrs={"data_see": "true"}))
    start_date = forms.DateField(required=False, label='Date de parution',
                                 widget=forms.DateInput(attrs={"type": "date", "data_see": "true"}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date", "data_see": "true"}))

    # Voir plus
    year_of_purchase = forms.IntegerField(required=False, label="Année d'achat",
                                          widget=forms.NumberInput(attrs={"data_see": "false"}))
    edition = forms.CharField(required=False, label='Édition', widget=forms.TextInput(attrs={"data_see": "false"}))
    deluxe_edition = forms.ChoiceField(
        required=False,
        label='Tirage de tête',
        choices=[
            ("", "Sélectionner une option"),
            ("True", "Oui"),
            ("False", "Non")
        ],
        widget=forms.Select(attrs={"data_see": "false", "class": "default-option"})
    )
    isbn = forms.IntegerField(required=False, label='ISBN', widget=forms.NumberInput(attrs={"data_see": "false"}))
    number = forms.CharField(required=False, label='Numéro', widget=forms.TextInput(attrs={"data_see": "false"}))
    synopsis = forms.CharField(required=False, label='Synopsis', widget=forms.TextInput(attrs={"data_see": "false"}))
