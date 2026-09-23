import os
import sys

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from main.core.domain.exceptions.album_exceptions import AlbumNotFoundException
from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.persistence.database.models import Collection, AppUser
from tests.album_data_set import ASTERIX


class AlbumInfosIntegrationTest(TestCase):
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
    @patch('main.core.infrastructure.interface_adapters.views.album_infos_view.GetInfosService.main')
    def test_album_infos_bd_success(self, mock_get_infos, mock_get_profile_type, mock_verify_token):
        mock_verify_token.return_value = self.collection
        mock_get_profile_type.return_value = ProfileType.BD
        mock_get_infos.return_value = ASTERIX

        response = self.client.get(
            reverse('album_infos', kwargs={'isbn': self.isbn}),
            **self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = response.json()
        self.assertEqual(data['isbn'], ASTERIX.isbn)
        self.assertEqual(data['title'], ASTERIX.title)
        self.assertEqual(data['series'], ASTERIX.series)

        mock_get_infos.assert_called_once_with(self.isbn)

    @patch('main.core.application.usecases.authorization.authorization_service.AuthorizationService.verify_token')
    @patch(
        'main.core.infrastructure.interface_adapters.profile_type.profile_type_adapter.ProfileTypeAdapter.get_profile_type')
    @patch('main.core.infrastructure.interface_adapters.views.album_infos_view.GetInfosService.main')
    def test_album_infos_book_success(self, mock_get_infos, mock_get_profile_type, mock_verify_token):
        mock_verify_token.return_value = self.collection
        mock_get_profile_type.return_value = ProfileType.BOOK
        mock_get_infos.return_value = ASTERIX

        response = self.client.get(
            reverse('album_infos', kwargs={'isbn': self.isbn}),
            **self.headers
        )

        self.assertEqual(response.status_code, 200)
        mock_get_infos.assert_called_once_with(self.isbn)

    @patch('main.core.application.usecases.authorization.authorization_service.AuthorizationService.verify_token')
    @patch(
        'main.core.infrastructure.interface_adapters.profile_type.profile_type_adapter.ProfileTypeAdapter.get_profile_type')
    @patch('main.core.infrastructure.interface_adapters.views.album_infos_view.GetInfosService.main')
    def test_album_infos_not_found(self, mock_get_infos, mock_get_profile_type, mock_verify_token):
        mock_verify_token.return_value = self.collection
        mock_get_profile_type.return_value = ProfileType.BD
        mock_get_infos.side_effect = AlbumNotFoundException("not found", self.isbn)

        response = self.client.get(
            reverse('album_infos', kwargs={'isbn': self.isbn}),
            **self.headers
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn("introuvable", response.content.decode())

    @patch('main.core.application.usecases.authorization.authorization_service.AuthorizationService.verify_token')
    @patch(
        'main.core.infrastructure.interface_adapters.profile_type.profile_type_adapter.ProfileTypeAdapter.get_profile_type')
    @patch('main.core.infrastructure.interface_adapters.views.album_infos_view.GetInfosService.main')
    def test_album_infos_server_error(self, mock_get_infos, mock_get_profile_type, mock_verify_token):
        mock_verify_token.return_value = self.collection
        mock_get_profile_type.return_value = ProfileType.BD
        mock_get_infos.side_effect = Exception("boom")

        response = self.client.get(
            reverse('album_infos', kwargs={'isbn': self.isbn}),
            **self.headers
        )

        self.assertEqual(response.status_code, 500)

    def test_album_infos_without_authorization_header(self):
        response = self.client.get(
            reverse('album_infos', kwargs={'isbn': self.isbn})
        )

        self.assertEqual(response.status_code, 403)

    def test_album_infos_with_unknown_token(self):
        response = self.client.get(
            reverse('album_infos', kwargs={'isbn': self.isbn}),
            HTTP_AUTHORIZATION='Bearer unknown-token'
        )

        self.assertEqual(response.status_code, 403)

    @patch('main.core.application.usecases.authorization.authorization_service.AuthorizationService.verify_token')
    def test_album_infos_method_not_allowed(self, mock_verify_token):
        mock_verify_token.return_value = self.collection

        response = self.client.post(
            reverse('album_infos', kwargs={'isbn': self.isbn}),
            **self.headers
        )

        self.assertEqual(response.status_code, 405)
