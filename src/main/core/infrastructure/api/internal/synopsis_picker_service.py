import re


class SynopsisPickerService:
    # Mots très courants en français et rares dans les autres langues des fiches Google Books
    FRENCH_WORDS = {
        "le", "la", "les", "un", "une", "des", "du", "et", "est", "dans", "au", "aux", "ce", "cette",
        "ces", "qui", "que", "il", "elle", "ils", "elles", "son", "sa", "ses", "sur", "pour", "par",
        "pas", "ne", "plus", "avec", "se", "leur", "je", "nous", "vous", "mais", "où", "à",
    }
    WORD_PATTERN = re.compile(r"[a-zà-ÿœæ]+")

    @classmethod
    def french_score(cls, text: str) -> float:
        words = cls.WORD_PATTERN.findall(text.lower())
        if not words:
            return 0.0
        return sum(word in cls.FRENCH_WORDS for word in words) / len(words)

    @classmethod
    def pick(cls, candidates: list[str]) -> str:
        """Garde le synopsis le plus français ; à score égal, le premier de la liste."""
        synopses = [candidate for candidate in candidates if candidate]
        if not synopses:
            return ""
        return max(synopses, key=cls.french_score)
