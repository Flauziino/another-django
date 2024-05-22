from apostilas.tests.test_base import BaseTestMixin
from usuarios import views

from django.urls import reverse, resolve


class LogarViewTest(BaseTestMixin):
    # METHOD GET
    def test_logar_view_is_correct(self):
        view = resolve(reverse('login'))

        self.assertIs(view.func, views.logar)

    def test_logar_view_status_code_200(self):
        url = reverse('login')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_logar_view_uses_right_template(self):
        url = reverse('login')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'login.html')

    # METHOD POST
    def test_logar_view_method_post_receive_wrong_credentials_and_redirect(self):  # noqa: E501
        user = self.get_user()

        logar_data = {
            'username': user.username,
            'senha': '12345',
        }

        url = reverse('login')
        response = self.client.post(url, data=logar_data, follow=True)

        self.assertRedirects(response, reverse('login'))

    def test_logar_view_method_post_receive_wrong_credentials_and_have_the_error_msg(self):  # noqa: E501
        user = self.get_user()

        logar_data = {
            'username': user.username,
            'senha': '12345',
        }

        url = reverse('login')
        response = self.client.post(url, data=logar_data, follow=True)

        self.assertIn(
            'Username ou senha invalidos',
            response.content.decode('utf-8')
        )

    def test_logar_view_method_post_receive_right_credentials_and_redirect(self):  # noqa: E501
        user = self.get_user()

        logar_data = {
            'username': user.username,
            'senha': '123456',
        }

        url = reverse('login')
        response = self.client.post(url, data=logar_data, follow=True)

        self.assertRedirects(response, '/flashcard/novo_flashcard/')

    def test_logar_view_method_post_receive_right_credentials_and_have_success_msg(self):  # noqa: E501
        user = self.get_user()

        logar_data = {
            'username': user.username,
            'senha': '123456',
        }

        url = reverse('login')
        response = self.client.post(url, data=logar_data, follow=True)

        self.assertIn(
            'Usuario logado com sucesso!',
            response.content.decode('utf-8')
        )
