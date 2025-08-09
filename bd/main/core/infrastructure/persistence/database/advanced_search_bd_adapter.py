import re
from abc import ABC
from typing import Any
from typing import Set

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import QuerySet, Q
from django.db.models import Value, Func
from django.db.models.functions import Lower

from main.core.domain.ports.repositories.advanced_search_repository import AdvancedSearchRepository
from main.core.infrastructure.persistence.database.models.bd import BD


class AdvancedSearchBdAdapter(AdvancedSearchRepository, ABC):

    def get_all(self, collection_id: int) -> QuerySet[BD, BD]:
        return BD.objects.filter(collection=collection_id)

    def get_by_form(self, data: dict[str, Any], queryset: QuerySet[BD, BD]) -> QuerySet[BD, BD]:
        queryset = self.filter_contains(data, queryset)
        queryset = self.filter_equals(data, queryset)
        queryset = self.filter_synopsis(data, queryset)
        queryset = self.filter_date(data, queryset)

        return queryset

    def filter_date(self, data, queryset):
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if start_date and end_date:
            queryset = queryset.filter(publication_date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(publication_date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(publication_date__lte=end_date)
        return queryset

    def filter_synopsis(self, data, queryset):
        if synopsis := data.get('synopsis'):
            queryset = self._search_synopsis(queryset, synopsis)
        return queryset

    def filter_equals(self, data, queryset):
        filter_equals_mappings = {
            'isbn': 'isbn',
            'year_of_purchase': 'year_of_purchase',
            'deluxe_edition': 'deluxe_edition',
        }
        for form_field, model_fields in filter_equals_mappings.items():
            value = data.get(form_field)
            if value is not None and value != '':
                queryset = queryset.filter(**{model_fields: value})
        return queryset

    def filter_contains(self, data, queryset):
        filter_contains_mappings = {
            'album': ['album', 'series', 'number'],
            'number': ['number'],
            'series': ['series'],
            'writer': ['writer'],
            'illustrator': ['illustrator'],
            'publisher': ['publisher'],
            'edition': ['edition'],
        }

        onomastic_search = ['album',
                            'series',
                            'writer',
                            'illustrator',
                            'publisher',
                            'edition']

        for form_field, model_fields in filter_contains_mappings.items():
            value = data.get(form_field)
            if value is not None and value != '':
                if isinstance(value, str):
                    search_terms = value.lower().split()
                else:
                    search_terms = [value]

                # Créer un filtre global pour tous les termes
                global_filter = Q()

                # Pour chaque terme de recherche
                for term in search_terms:
                    term_filter = Q()

                    # Pour chaque champ à rechercher
                    for model_field in model_fields:
                        if model_field in onomastic_search:
                            # Annotation pour le champ sans accents
                            annotated_queryset = queryset.annotate(**{
                                f"unaccented_{model_field}": Func(
                                    Lower(model_field),
                                    function="unaccent"
                                )
                            })

                            # Condition pour ce terme dans ce champ
                            search_condition = Q(**{
                                f"unaccented_{model_field}__icontains": Func(
                                    Value(term),
                                    function="unaccent"
                                )
                            })

                            # Ajouter au filtre du terme (OR entre les champs)
                            term_filter |= Q(
                                id__in=annotated_queryset.filter(search_condition).values('id')
                            )
                        else:
                            term_filter |= Q(**{f"{model_field}__icontains": term})

                    # AND entre les termes
                    global_filter &= term_filter

                # Appliquer le filtre global
                queryset = queryset.filter(global_filter)
        return queryset

    # Liste des mots vides en français
    STOP_WORDS: Set[str] = {
        # Ponctuation
        "...",
        # Articles
        'le', 'la', 'les', 'l', 'un', 'une', 'des', 'du', 'au', 'aux',
        # Pronoms
        'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
        'me', 'te', 'se', 'lui', 'leur', 'eux',
        'moi', 'toi', 'soi', 'celui', 'celle', 'ceux', 'celles',
        'ce', 'cette', 'ces', 'mon', 'ton', 'son', 'notre', 'votre', 'leur',
        'ma', 'ta', 'sa', 'mes', 'tes', 'ses', 'nos', 'vos', 'leurs',
        # Prépositions
        'à', 'de', 'dans', 'chez', 'sur', 'sous', 'vers', 'par', 'pour',
        'en', 'entre', 'derrière', 'devant', 'avec', 'sans', 'contre',
        # Conjonctions
        'et', 'ou', 'mais', 'donc', 'or', 'ni', 'car', 'que', 'qui', 'quoi',
        'dont', 'où', 'quand', 'comment', 'pourquoi', 'si',
        # Adverbes communs
        'très', 'bien', 'peu', 'plus', 'moins', 'aussi', 'trop',
        'assez', 'tout', 'tous', 'toute', 'toutes',
        # Verbes être et avoir (formes courantes)
        'est', 'sont', 'était', 'être', 'suis', 'es', 'sommes', 'êtes',
        'a', 'ont', 'avait', 'avoir', 'ai', 'as', 'avons', 'avez',
        # Autres mots fréquents peu significatifs
        'fait', 'faire', 'comme', 'alors', 'après', 'avant', 'pendant',
        'puis', 'car', 'donc', 'cependant', 'néanmoins',
    }

    def _divide_search_terms(self, text: str):
        """
        Divise le texte en mots et nettoie chaque mot
        """

        ponctuation = [',', ';', ':', '!', '?', '.', '"', "'", '(', ')', '[', ']', '{', '}', '/', '\\', '-', '_']
        # Remplacer la ponctuation par des espaces
        for p in ponctuation:
            text = text.replace(p, ' ')

        words = [
            word.strip().lower()
            for word in text.split()
            if word.strip()
        ]

        # Nettoie chaque mot des caractères spéciaux
        cleaned_words = []
        for word in words:
            # Garde uniquement les lettres et les chiffres
            cleaned_word = re.sub(r'[^a-zA-Z0-9àáâãäçèéêëìíîïñòóôõöùúûüýÿ]', '', word)
            if cleaned_word:  # Si le mot n'est pas vide après nettoyage
                cleaned_words.append(cleaned_word)

        return cleaned_words

    def _clean_search_terms(self, words: list[str]) -> list[str]:
        """
        Filtre les termes de recherche en enlevant les mots vides
        """
        return [
            word for word in words
            if word not in self.STOP_WORDS and len(word) > 2
        ]

    def _search_synopsis(self, queryset: QuerySet[BD, BD], synopsis: str) -> QuerySet[BD, BD]:
        """
        Recherche avancée dans le synopsis avec gestion des caractères spéciaux et de la pertinence
        """
        if not synopsis:
            return queryset

        # Nettoyage et préparation des mots de recherche
        words = self._divide_search_terms(synopsis)
        original_words = words.copy()
        words = self._clean_search_terms(words)

        # Si tous les mots sont filtrés, mais qu'il y avait des mots dans la recherche originale
        if not words and original_words:
            # Utiliser les mots originaux si leur longueur est significative (> 2 caractères)
            search_words = [w for w in original_words if len(w) > 2]
            if search_words:
                words = search_words
            else:
                return queryset.none()

        # Création de l'annotation une seule fois pour le champ sans accents
        queryset = queryset.annotate(
            clean_synopsis=Func(
                Lower('synopsis'),
                function='unaccent'
            )
        )

        # Construction de la requête
        base_query = Q()
        for word in words:
            # Création d'une sous-requête pour chaque mot
            word_query = Q()

            # Recherche exacte
            word_query |= Q(clean_synopsis__icontains=Func(
                Value(word),
                function='unaccent'
            ))

            # Recherche avec flexibilité sur la fin du mot (ex: "aventur" trouvera "aventure", "aventurier")
            if len(word) > 3:  # Pour éviter les faux positifs sur les mots courts
                word_query |= Q(clean_synopsis__icontains=Func(
                    Value(word[:-1]),  # On enlève le dernier caractère
                    function='unaccent'
                ))

            base_query &= word_query

        # Application de la requête avec ordre de pertinence
        queryset = queryset.filter(base_query)

        # Tri par pertinence si PostgreSQL est utilisé
        try:
            search_vector = SearchVector('synopsis', config='french')
            search_query = ' & '.join(words)  # Connexion AND entre les mots
            search_rank = SearchRank(search_vector, SearchQuery(search_query, config='french'))

            queryset = queryset.annotate(
                rank=search_rank
            ).order_by('-rank')
        except Exception:
            # Fallback si la fonctionnalité de recherche full-text n'est pas disponible
            pass

        return queryset
