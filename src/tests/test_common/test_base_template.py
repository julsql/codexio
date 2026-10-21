import os
import sys

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.template.loader import render_to_string
from django.test import SimpleTestCase


class BaseTemplateTest(SimpleTestCase):
    def test_base_template_includes_umami_tracker(self):
        html = render_to_string('main/base.html')

        head = html.split('</head>')[0]
        self.assertIn('src="https://stats.julsql.fr/js/app.js"', head)
        self.assertIn('data-website-id="48d17bf6-9a55-459d-af16-42b3a9dd5c83"', head)
        self.assertIn('data-domains="codexio.julsql.fr"', head)
