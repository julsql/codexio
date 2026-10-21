import json
import os
import re
import sys

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from unittest.mock import patch

from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse

from main.core.infrastructure.persistence.database.models import AppUser

SITE_URL = 'https://codexio.julsql.fr'


class LandingPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_landing_is_public(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing/module.html')

    def test_landing_has_login_and_demo_actions(self):
        content = self.client.get('/').content.decode()
        self.assertIn(f'href="{reverse("login")}"', content)
        self.assertIn(f'action="{reverse("demo_login")}"', content)

    def test_landing_has_seo_tags(self):
        content = self.client.get('/').content.decode()
        title = re.search(r'<title>(.*?)</title>', content).group(1)
        description = re.search(r'<meta name="description" content="(.*?)"/>', content).group(1)
        self.assertTrue(50 <= len(title) <= 60, title)
        self.assertTrue(140 <= len(description) <= 160, description)
        self.assertIn(f'<link rel="canonical" href="{SITE_URL}/"/>', content)
        self.assertNotIn('noindex', content)
        for prop in ('og:title', 'og:description', 'og:url', 'og:type', 'og:locale'):
            self.assertIn(f'property="{prop}"', content)
        self.assertIn(f'property="og:image" content="{SITE_URL}/static/main/images/og-image.png"', content)
        self.assertIn('name="twitter:card"', content)
        self.assertIn('rel="apple-touch-icon"', content)
        self.assertIn('name="theme-color"', content)
        self.assertIn('<html lang="fr">', content)

    def test_landing_has_a_single_h1(self):
        content = self.client.get('/').content.decode()
        self.assertEqual(content.count('<h1'), 1)

    def test_landing_json_ld_is_valid(self):
        content = self.client.get('/').content.decode()
        raw = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.S).group(1)
        types = {node['@type'] for node in json.loads(raw)['@graph']}
        self.assertEqual(types, {'WebSite', 'WebApplication'})

    @patch('main.core.infrastructure.interface_adapters.views.home_view.HomeView.handle_request')
    def test_authenticated_user_keeps_dashboard(self, mock_handle_request):
        mock_handle_request.return_value = HttpResponse('dashboard')
        self.client.force_login(AppUser.objects.get(username='admin'))
        response = self.client.get('/')
        self.assertEqual(response.content, b'dashboard')
        mock_handle_request.assert_called_once()


class LoginPageSeoTest(TestCase):
    def test_login_page_has_title_description_and_canonical(self):
        content = Client().get(reverse('login')).content.decode()
        title = re.search(r'<title>(.*?)</title>', content).group(1)
        description = re.search(r'<meta name="description"\s+content="(.*?)"/>', content).group(1)
        self.assertTrue(50 <= len(title) <= 60, title)
        self.assertTrue(140 <= len(description) <= 160, description)
        self.assertIn(f'<link rel="canonical" href="{SITE_URL}/accounts/login/"/>', content)


class RobotsAndSitemapTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_robots_txt(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain; charset=utf-8')
        content = response.content.decode()
        self.assertIn('Allow: /\n', content)
        for path in ('/admin/', '/accounts/', '/recherche/', '/ouvrage/', '/infos/'):
            self.assertIn(f'Disallow: {path}\n', content)
        self.assertIn(f'Sitemap: {SITE_URL}/sitemap.xml', content)

    def test_sitemap_xml(self):
        response = self.client.get('/sitemap.xml', HTTP_HOST='codexio.julsql.fr')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        content = response.content.decode()
        self.assertIn(f'<loc>{SITE_URL}/</loc>', content)
        self.assertIn(f'<loc>{SITE_URL}/accounts/login/</loc>', content)
        self.assertNotIn('/recherche/', content)


class PrivateViewsStayProtectedTest(TestCase):
    PRIVATE_URLS = [
        '/profile',
        '/recherche/',
        '/dedicaces/',
        '/exlibris/',
        '/statistiques/',
        '/ouvrage/1234567890/',
        '/change-collection/1/',
    ]

    def test_anonymous_is_redirected_to_login(self):
        client = Client()
        for url in self.PRIVATE_URLS:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response['Location'].startswith(reverse('login')))

    def test_token_api_rejects_anonymous(self):
        response = Client().get(reverse('album_infos', kwargs={'isbn': 1234567890}))
        self.assertNotEqual(response.status_code, 200)
