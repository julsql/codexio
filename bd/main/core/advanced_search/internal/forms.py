from dataclasses import field

from django import forms
from django.forms import CheckboxInput
from django.utils.safestring import mark_safe

class RechercheForm(forms.Form):
    series = forms.CharField(required=False, label='Série', widget=forms.TextInput(attrs={'placeholder': 'Série'}))
    album = forms.CharField(required=False, label='Album', widget=forms.TextInput(attrs={'placeholder': 'Album'}))
    writer = forms.CharField(required=False, label='Scénariste', widget=forms.TextInput(attrs={'placeholder': 'Scénariste'}))
    illustrator = forms.CharField(required=False, label='Dessinateur', widget=forms.TextInput(attrs={'placeholder': 'Dessinateur'}))
    publisher = forms.CharField(required=False, label='Éditeur', widget=forms.TextInput(attrs={'placeholder': 'Éditeur'}))
    publication_date = forms.CharField(required=False, label='Date de parution', widget=forms.TextInput(attrs={'placeholder': 'Date de parution'}))

    # Voir plus
    year_of_purchase = forms.CharField(required=False, label="Année d'achat", widget=forms.TextInput(attrs={'placeholder': "Année d'achat"}))
    edition = forms.CharField(required=False, label='Édition', widget=forms.TextInput(attrs={'placeholder': 'Édition'}))
    deluxe_edition = forms.CharField(required=False, label='Tirage de tête', widget=forms.TextInput(attrs={'placeholder': 'Tirage de tête'}))
    isbn = forms.CharField(required=False, label='ISBN', widget=forms.TextInput(attrs={'placeholder': 'ISBN'}))
    number = forms.CharField(required=False, label='Numéro', widget=forms.TextInput(attrs={'placeholder': 'Numéro'}))
    synopsis = forms.CharField(required=False, label='Synopsis', widget=forms.TextInput(attrs={'placeholder': 'Synopsis'}))

    # Méthode pour afficher le formulaire sous forme de tableau (optionnel)
    def as_custom_table_2(self) -> str:
        html = '\t<table>\n'
        html += '\t\t\t\t\t<tr>\n'
        i = 0
        for field in self:
            if i % 2 == 0 and i > 0:
                html += '\t\t\t\t\t</tr>\n'
                html += '\t\t\t\t\t<tr>\n'

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
