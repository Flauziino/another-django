from apostilas.tests.test_base import BaseTestMixin
from usuarios import views

from django.urls import reverse, resolve


class LogoutViewTest(BaseTestMixin):
    # METHOD GET
    def test_logout_view_is_correct(self):
        view = resolve(reverse('logout'))

        self.assertIs(view.func, views.logout)

    def test_logout_view_logout_user_and_redirect(self):
        user = self.get_user()
        self.client.force_login(user)

        url = reverse('logout')
        response = self.client.get(url)

        self.assertRedirects(response, reverse('login'))

    def test_logout_view_logout_user_and_have_success_msg(self):
        user = self.get_user()
        self.client.force_login(user)

        url = reverse('logout')
        response = self.client.get(url, follow=True)

        self.assertIn(
            'Usuario deslogado com sucesso, volte sempre!',
            response.content.decode('utf-8')
        )

    def test_logout_view_is_all_good_together_with_login_view(self):
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

        url = reverse('logout')
        response = self.client.get(url, follow=True)

        self.assertIn(
            'Usuario deslogado com sucesso, volte sempre!',
            response.content.decode('utf-8')
        )
