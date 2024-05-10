from apostilas.tests.test_base import BaseTestMixin
from apostilas.models import Avaliacao
from apostilas import views

from django.urls import reverse, resolve


class ApostilaViewTest(BaseTestMixin):
    def test_apostila_view_is_correct(self):
        view = resolve(reverse('apostila', kwargs={'id': 1}))

        self.assertIs(view.func, views.apostila)

    def test_apostila_view_method_get_return_status_code_200(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('apostila', kwargs={'id': apostila.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_apostila_view_method_get_use_right_template(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('apostila', kwargs={'id': apostila.id})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'apostila.html')

    def test_apostila_view_have_apostila_on_context(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('apostila', kwargs={'id': apostila.id})
        response = self.client.get(url)

        self.assertIn('apostila', response.context)

    def test_apostila_view_have_views_unicas_on_context(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('apostila', kwargs={'id': apostila.id})
        response = self.client.get(url)

        self.assertIn('views_unicas', response.context)

    def test_apostila_view_have_views_totais_on_context(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('apostila', kwargs={'id': apostila.id})
        response = self.client.get(url)

        self.assertIn('views_totais', response.context)

    def test_apostila_view_have_total_avaliacoes_on_context(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('apostila', kwargs={'id': apostila.id})
        response = self.client.get(url)

        self.assertIn('total_avaliacoes', response.context)

    def test_apostila_view_have_proporcao_ruim_on_context(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('apostila', kwargs={'id': apostila.id})
        response = self.client.get(url)

        self.assertIn('proporcao_ruim', response.context)

    def test_apostila_view_have_proporcao_bom_on_context(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('apostila', kwargs={'id': apostila.id})
        response = self.client.get(url)

        self.assertIn('proporcao_bom', response.context)

    def test_apostila_view_have_proporcao_otimo_on_context(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('apostila', kwargs={'id': apostila.id})
        response = self.client.get(url)

        self.assertIn('proporcao_otimo', response.context)

    def test_apostila_view_have_maior_avaliacao_on_context(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('apostila', kwargs={'id': apostila.id})
        response = self.client.get(url)

        self.assertIn('maior_avaliacao', response.context)

    def test_apostila_view_method_post_return_status_code_200(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('apostila', kwargs={'id': apostila.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

    def test_apostila_view_method_post_receive_avaliacao_and_create_avaliacao_and_redirects(self):  # noqa:E501
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        data = {
            'avaliacao': 'bom'
        }

        url = reverse('apostila', kwargs={'id': apostila.id})
        response = self.client.post(url, data=data)

        avaliacao = Avaliacao.objects.all().first()

        self.assertEqual(
            str(avaliacao), 'bom'
        )
        self.assertRedirects(
            response,
            reverse('apostila', kwargs={'id': apostila.id})
        )
