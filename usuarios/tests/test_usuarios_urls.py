from django.test import TestCase
from django.urls import reverse


class UsuariosURLsTest(TestCase):

    def test_cadastro_urls_is_correct(self):
        url = reverse('cadastro')
        self.assertEqual(url, '/usuarios/cadastro/')

    def test_login_url_is_correct(self):
        url = reverse('login')
        self.assertEqual(url, '/usuarios/logar/')

    def test_logout_url_is_correct(self):
        url = reverse('logout')
        self.assertEqual(url, '/usuarios/logout/')
