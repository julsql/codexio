from django import forms
from django.forms import CheckboxInput
from django.utils.safestring import mark_safe

class RechercheForm(forms.Form):
    isbn = forms.CharField(required=False, label='ISBN', widget=forms.TextInput(attrs={'placeholder': 'ISBN'}))
    album = forms.CharField(required=False, label='Album', widget=forms.TextInput(attrs={'placeholder': 'Album'}))
    number = forms.CharField(required=False, label='Numéro', widget=forms.TextInput(attrs={'placeholder': 'Numéro'}))
    series = forms.CharField(required=False, label='Série', widget=forms.TextInput(attrs={'placeholder': 'Série'}))
    writer = forms.CharField(required=False, label='Scénariste', widget=forms.TextInput(attrs={'placeholder': 'Scénariste'}))
    illustrator = forms.CharField(required=False, label='Dessinateur', widget=forms.TextInput(attrs={'placeholder': 'Dessinateur'}))
    publisher = forms.CharField(required=False, label='Éditeur', widget=forms.TextInput(attrs={'placeholder': 'Éditeur'}))
    edition = forms.CharField(required=False, label='Édition', widget=forms.TextInput(attrs={'placeholder': 'Édition'}))
    year_of_purchase = forms.CharField(required=False, label="Année d'achat", widget=forms.TextInput(attrs={'placeholder': "Année d'achat"}))
    signed_copy = forms.CharField(required=False, label='Dédicace', widget=forms.TextInput(attrs={'placeholder': 'Dédicace'}))
    ex_libris = forms.CharField(required=False, label='Ex Libris', widget=forms.TextInput(attrs={'placeholder': 'Ex Libris'}))
    synopsis = forms.CharField(required=False, label='Synopsis', widget=forms.TextInput(attrs={'placeholder': 'Synopsis'}))

    # Options de tri mises à jour avec les nouveaux champs du modèle
    TRI_CHOICES = [
        ('album', 'Album'),
        ('number', 'Numéro'),
        ('series', 'Série'),
        ('publication_date', 'Date de parution'),
        ("year_of_purchase", "Année d'achat"),
        ('number_of_pages', 'Nombre de pages'),
        ("place_of_purchase", "Lieu d'achat"),
        ('illustrator', 'Dessinateur'),
        ('writer', 'Scénariste'),
    ]

    tri_par = forms.ChoiceField(
        label='Trier par',
        choices=[('', '--- Sélectionner ---')] + TRI_CHOICES,
        required=False,  # Rend le champ facultatif
    )

    tri_croissant = forms.BooleanField(
        required=False,
        label='↓',
        widget=CheckboxInput(attrs={'class': 'custom-checkbox'}),
    )

    # Méthode pour afficher le formulaire sous forme de tableau (optionnel)
    def as_custom_table_2(self) -> str:
        html = '\t<table>\n'
        html += '\t\t\t\t\t<tr>\n'
        i = 0
        for field in self:
            if i % 2 == 0 and i > 0:
                html += '\t\t\t\t\t</tr>\n'
                html += '\t\t\t\t\t<tr>\n'

            if field.id_for_label == "id_tri_par":
                html += f'\t\t\t\t\t\t<td><label for="{field.id_for_label}">{field.label}&nbsp;:</label></td>\n'
                html += f'\t\t\t\t\t\t<td>{field}\n'
            elif field.id_for_label == "id_tri_croissant":
                html += f'\t\t\t\t\t\t<label for="{field.id_for_label}">{field.label}</label>{field}</td>\n'
            else:
                html += f'\t\t\t\t\t\t<td><label for="{field.id_for_label}">{field.label}&nbsp;:</label></td>\n'
                html += f'\t\t\t\t\t\t<td>{field}</td>\n'

            i += 1

        html += '\t\t\t\t\t</tr>\n'
        html += '\t\t\t\t</table>\n'

        return mark_safe(html)

    def as_custom_table_3(self) -> str:
        html = '\t<table>\n'
        html += '\t\t\t\t\t<tr>\n'
        i = 0
        for field in self:
            if i % 3 == 0 and i > 0:
                html += '\t\t\t\t\t</tr>\n'
                html += '\t\t\t\t\t<tr>\n'

            if field.id_for_label == "id_tri_par":
                html += f'\t\t\t\t\t\t<td><label for="{field.id_for_label}">{field.label}&nbsp;:</label></td>\n'
                html += f'\t\t\t\t\t\t<td>{field}\n'
            elif field.id_for_label == "id_tri_croissant":
                html += f'\t\t\t\t\t\t<label for="{field.id_for_label}">{field.label}</label>{field}</td>\n'
            else:
                html += f'\t\t\t\t\t\t<td><label for="{field.id_for_label}">{field.label}&nbsp;:</label></td>\n'
                html += f'\t\t\t\t\t\t<td>{field}</td>\n'

            i += 1

        html += '\t\t\t\t</table>\n'

        return mark_safe(html)
