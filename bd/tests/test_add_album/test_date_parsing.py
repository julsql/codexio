import unittest

from main.core.add_album.internal.bdgest_connexion import BdGestRepository


class TestDateParsing(unittest.TestCase):
    def setUp(self):
        self.repo = BdGestRepository()

    def test_parse_publication_date(self):
        test_cases = [
            # Format avec point (BDFugue)
            {
                "input": "8 févr. 2023",
                "expected": "2023-02-08"
            },
            # Format complet français
            {
                "input": "8 février 2023",
                "expected": "2023-02-08"
            },
            # Format déjà ISO
            {
                "input": "2023-08-01",
                "expected": "2023-08-01"
            },
            # Format avec mois courts
            {
                "input": "15 janv. 2023",
                "expected": "2023-01-15"
            },
            {
                "input": "21 mars 2023",
                "expected": "2023-03-21"
            },
            {
                "input": "30 avr. 2023",
                "expected": "2023-04-30"
            },
            {
                "input": "1 juin 2023",
                "expected": "2023-06-01"
            },
            {
                "input": "5 juil. 2023",
                "expected": "2023-07-05"
            },
            {
                "input": "12 août 2023",
                "expected": "2023-08-12"
            },
            {
                "input": "25 sept. 2023",
                "expected": "2023-09-25"
            },
            {
                "input": "17 oct. 2023",
                "expected": "2023-10-17"
            },
            {
                "input": "3 nov. 2023",
                "expected": "2023-11-03"
            },
            {
                "input": "28 déc. 2023",
                "expected": "2023-12-28"
            },
            # formats incomplets
            {
                "input": "2024-03-15",
                "expected": "2024-03-15"
            },
            {
                "input": "2024-03",
                "expected": "2024-03-01"
            },
            {
                "input": "2024",
                "expected": "2024-01-01"
            },
            {
                "input": "Mars 2024",
                "expected": "2024-03-01"
            },
            {
                "input": "15 Mars 2024",
                "expected": "2024-03-15"
            },
            {
                "input": "2024-3-15",
                "expected": "2024-03-15"
            },
            {
                "input": "15/03/2024",
                "expected": "2024-03-15"
            }
        ]

        for test_case in test_cases:
            with self.subTest(input=test_case["input"]):
                informations = {"Date de publication": test_case["input"]}
                self.repo._parse_publication_date(informations, "123")
                self.assertEqual(
                    informations["Date de publication"],
                    test_case["expected"],
                    f"Failed to parse {test_case['input']} correctly"
                )

    def test_translate_method(self):
        test_cases = [
            ("8 février 2023", "8 February 2023"),
            ("15 mars 2023", "15 March 2023"),
            ("21 avril 2023", "21 April 2023"),
            ("1 mai 2023", "1 May 2023"),
            ("30 juin 2023", "30 June 2023"),
            ("12 juillet 2023", "12 July 2023"),
            ("25 août 2023", "25 August 2023"),
            ("18 septembre 2023", "18 September 2023"),
            ("5 octobre 2023", "5 October 2023"),
            ("23 novembre 2023", "23 November 2023"),
            ("31 décembre 2023", "31 December 2023")
        ]

        for input_date, expected in test_cases:
            with self.subTest(input=input_date):
                result = self.repo.translate(input_date)
                self.assertEqual(
                    result,
                    expected,
                    f"Failed to translate {input_date} correctly"
                )

    def test_translate_method(self):
        dates_test = [
            "2024-03-15",  # Date complète
            "2024-03",  # Année-mois
            "2024",  # Seulement année
            "Mars 2024",  # Mois textuel et année
            "15 Mars 2024",  # Date complète textuelle
            "2024-3-15",  # Format sans zéros
            "15/03/2024",  # Format avec slashes
        ]

        for date in dates_test:
            resultat = parse_date(date, "TEST-ISBN")
            print(f"\nDate originale : {date}")
            print(f"Date parsée : {resultat}")

    def test_invalid_dates(self):
        invalid_dates = [
            {"Date de publication": ""},  # Date vide
            {"Date de publication": "invalid"},  # Date invalide
            {"Date de publication": "2023/13/45"},  # Date impossible
            {"Date de publication": "35 février 2023"},  # Jour impossible
            {},  # Dictionnaire vide
        ]

        for test_case in invalid_dates:
            with self.subTest(input=test_case):
                informations = test_case.copy()
                self.repo._parse_publication_date(informations, "123")
                # Vérifie que la date n'a pas été modifiée ou a été supprimée
                if "Date de publication" in informations:
                    self.assertIsInstance(
                        informations["Date de publication"], str,
                        "Invalid date should remain a string or be removed"
                    )

    def test_edge_cases(self):
        edge_cases = [
            # Années limites
            {
                "input": "1 janvier 1900",
                "expected": "1900-01-01"
            },
            {
                "input": "31 décembre 2099",
                "expected": "2099-12-31"
            },
            # Casse mixte
            {
                "input": "15 FéVrIeR 2023",
                "expected": "2023-02-15"
            },
            # Espaces supplémentaires
            {
                "input": "  8  mars   2023  ",
                "expected": "2023-03-08"
            }
        ]

        for test_case in edge_cases:
            with self.subTest(input=test_case["input"]):
                informations = {"Date de publication": test_case["input"]}
                self.repo._parse_publication_date(informations, "123")
                self.assertEqual(
                    informations["Date de publication"],
                    test_case["expected"],
                    f"Failed to parse edge case {test_case['input']} correctly"
                )


if __name__ == '__main__':
    unittest.main()
