import os
import sys

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.persistence.database.models import Collection, AppUser


class AddAlbumIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.isbn = 1234567890
        self.token = 'Bearer test-token'
        self.headers = {'HTTP_AUTHORIZATION': self.token}

        user = AppUser.objects.get(username="admin")
        self.collection = Collection.objects.get(accounts=user)

    @patch('main.core.application.usecases.authorization.authorization_service.AuthorizationService.verify_token')
    @patch(
        'main.core.infrastructure.interface_adapters.profile_type.profile_type_adapter.ProfileTypeAdapter.get_profile_type')
    @patch('main.core.infrastructure.interface_adapters.views.add_album_view.AddBdService.main')
    def test_add_bd_success(self, mock_add_album, mock_get_profile_type, mock_verify_token):
        # Mock les méthodes nécessaires
        mock_verify_token.return_value = self.collection
        mock_get_profile_type.return_value = ProfileType.BD
        mock_add_album.return_value = None  # Pas d'erreur = succès

        # Effectuer une requête GET (ton endpoint utilise GET)
        response = self.client.get(
            reverse('add_album', kwargs={'isbn': self.isbn}),
            **self.headers
        )

        # Vérifie la réponse
        print("Response content:", response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("ajouté avec succès", response.content.decode())

        # Assure que la logique a été appelée
        mock_add_album.assert_called_once_with(self.isbn)
