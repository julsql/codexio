from django import forms
from django.utils.safestring import mark_safe

class RechercheForm(forms.Form):
    series = forms.CharField(required=False, label='Série', widget=forms.TextInput(attrs={"data_see": "true"}))
    album = forms.CharField(required=False, label='Album', widget=forms.TextInput(attrs={"data_see": "true"}))
    writer = forms.CharField(required=False, label='Scénariste', widget=forms.TextInput(attrs={"data_see": "true"}))
    illustrator = forms.CharField(required=False, label='Dessinateur', widget=forms.TextInput(attrs={ "data_see": "true"}))
    publisher = forms.CharField(required=False, label='Éditeur', widget=forms.TextInput(attrs={"data_see": "true"}))
    start_date = forms.DateField(required=False, label='Date de parution', widget=forms.DateInput(attrs={"type": "date", "data_see": "true"}))
    end_date = forms.DateField(required=False, label='Date de parution - fin', widget=forms.DateInput(attrs={"type": "date", "data_see": "true"}))

    # Voir plus
    year_of_purchase = forms.IntegerField(required=False, label="Année d'achat", widget=forms.TextInput(attrs={"data_see": "false"}))
    edition = forms.CharField(required=False, label='Édition', widget=forms.TextInput(attrs={"data_see": "false"}))
    deluxe_edition = forms.ChoiceField(
        required=False,
        label='Tirage de tête',
        choices=[
            ("", "Sélectionner une option"),  # Valeur vide pour None
            ("True", "Oui"),
            ("False", "Non")
        ],
        widget=forms.Select(attrs={"data_see": "false"})
    )
    isbn = forms.IntegerField(required=False, label='ISBN', widget=forms.TextInput(attrs={"data_see": "false"}))
    number = forms.CharField(required=False, label='Numéro', widget=forms.TextInput(attrs={"data_see": "false"}))
    synopsis = forms.CharField(required=False, label='Synopsis', widget=forms.TextInput(attrs={"data_see": "false"}))

    def as_custom_table_3(self) -> str:
        html = '\t<table>\n'
        html += '\t\t\t\t\t<tr>\n'
        i = 0
        for field in self:
            if i % 3 == 0 and i > 0:
                html += '\t\t\t\t\t</tr>\n'
                html += '\t\t\t\t\t<tr>\n'

            if field.label == "Date de parution":
                html += f'\t\t\t\t\t\t<td data_see="{field.field.widget.attrs.get("data_see", "")}"><label for="{field.id_for_label}">Date de parution</label>{field}\n'
                i -= 1
            elif field.label == "Date de parution - fin":
                html += f'\t\t\t\t\t\t{field}</td>\n'

            else:
                html += f'\t\t\t\t\t\t<td data_see="{field.field.widget.attrs.get("data_see", "")}"><label for="{field.id_for_label}">{field.label}</label>{field}</td>\n'

            i += 1

        html += '\t\t\t\t\t</tr>\n'
        html += '\t\t\t\t</table>\n'

        return mark_safe(html)
