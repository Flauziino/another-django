from apostilas.tests.test_base import BaseTestMixin, User
from usuarios import views

from django.urls import reverse, resolve
from django.contrib.messages import get_messages

from unittest.mock import patch


class CadastroViewTest(BaseTestMixin):
    # METHOD GET
    def test_cadastro_view_is_correct(self):
        view = resolve(reverse('cadastro'))

        self.assertIs(view.func.view_class, views.CadastroView)

    def test_cadastro_view_method_get_status_code_200(self):
        url = reverse('cadastro')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_cadastro_view_method_get_uses_the_right_template(self):
        url = reverse('cadastro')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'cadastro.html')

    # METHOD POST
    def test_cadastro_view_method_post_receive_empty_form(self):
        data = {
            'username': '',
            'senha': '',
            'confirmar_senha': ' '
        }

        url = reverse('cadastro')
        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(response.status_code, 302)

    def test_cadastro_view_method_post_dont_receive_username(self):
        data = {
            'username': '',
            'senha': '1234',
            'confirmar_senha': '1234'
        }

        url = reverse('cadastro')
        response = self.client.post(
            url,
            data=data,
            follow=True
        )

        self.assertRedirects(response, '/usuarios/cadastro/')

    def test_cadastro_view_method_post_dont_receive_senha(self):
        data = {
            'username': 'user_test',
            'senha': '',
            'confirmar_senha': ''
        }

        url = reverse('cadastro')
        response = self.client.post(
            url,
            data=data,
            follow=True
        )

        self.assertRedirects(response, '/usuarios/cadastro/')

    def test_cadastro_view_method_post_senhas_nao_coincidem(self):
        data = {
            'username': 'user_test',
            'senha': '12345',
            'confirmar_senha': '1234'
        }

        url = reverse('cadastro')
        response = self.client.post(
            url,
            data=data,
            follow=True
        )

        self.assertRedirects(response, '/usuarios/cadastro/')
        self.assertIn(
            'As senhas nao coincidem',
            response.content.decode('utf-8')
        )

    def test_cadastro_view_method_post_create_a_user(self):
        data = {
            'username': 'user_test',
            'senha': '12345',
            'confirmar_senha': '12345'
        }

        url = reverse('cadastro')
        response = self.client.post(
            url,
            data=data,
            follow=True
        )

        new_user = User.objects.get(username='user_test')

        self.assertRedirects(response, reverse('login'))
        self.assertEqual(new_user.username, data['username'])
        self.assertIn(
            f'Usuario criado {data["username"]} com sucesso',
            response.content.decode('utf-8')
        )

    def test_cadastro_view_method_post_user_already_exists(self):
        data = {
            'username': 'user_test',
            'senha': '12345',
            'confirmar_senha': '12345'
        }

        user = User.objects.create_user(
            username='user_test',
            password='12345'
        )
        user.save()

        url = reverse('cadastro')
        response = self.client.post(
            url,
            data=data,
            follow=True
        )

        self.assertRedirects(response, '/usuarios/cadastro/')
        self.assertIn(
            'Esse nome de usuario ja existe',
            response.content.decode('utf-8')
        )

    @patch('django.contrib.auth.models.User.objects.create_user')
    def test_cadastro_view_method_post_create_user_exception(self, mock_create_user):  # noqa: E501
        # Configura o mock para levantar uma exceção
        mock_create_user.side_effect = Exception("Simulated exception")

        data = {
            'username': 'user_test',
            'senha': '12345',
            'confirmar_senha': '12345'
        }

        url = reverse('cadastro')
        response = self.client.post(url, data=data, follow=True)

        # Verifica o redirecionamento
        self.assertRedirects(response, reverse('cadastro'))

        # Verifica a mensagem de erro
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Erro interno do servidor')

        # Verifica que o usuário não foi criado
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='user_test')
