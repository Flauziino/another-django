from apostilas.tests.test_base import BaseTestMixin
from apostilas.models import Apostila, ViewApostila
from apostilas import views

from django.urls import reverse, resolve


class AdicionarApostilasViewTest(BaseTestMixin):
    def test_adicionar_apostila_view_is_correct(self):
        view = resolve(reverse('adicionar_apostilas'))

        self.assertIs(view.func, views.adicionar_apostilas)

    def test_adicionar_apostila_view_method_get_return_status_code_200(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('adicionar_apostilas')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_adicionar_apostila_view_method_get_return_right_template(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('adicionar_apostilas')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'adicionar_apostilas.html')

    def test_adicionar_apostila_view_method_get_return_apostilas_in_context(self):  # noqa:E501
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('adicionar_apostilas')
        response = self.client.get(url)

        self.assertIn('apostilas', response.context)

    def test_adicionar_apostila_view_method_get_return_views_totais_in_context(self):  # noqa:E501
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('adicionar_apostilas')
        response = self.client.get(url)

        self.assertIn('views_totais', response.context)

    def test_adicionar_apostila_view_method_get_the_content_of_context_apostilas_is_right(self):  # noqa:E501
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        query_for_test = Apostila.objects.filter(user=user)

        url = reverse('adicionar_apostilas')
        response = self.client.get(url)

        self.assertEqual(
            response.context['apostilas'].first(),
            query_for_test.first()
        )

    def test_adicionar_apostila_view_method_get_the_content_of_context_views_totais_is_right(self):  # noqa:E501
        view_apostila = self.make_view_apostila()
        user = view_apostila.apostila.user
        self.client.force_login(user)

        query_for_test = (
            ViewApostila.objects.filter(apostila__user=user).count()
        )

        url = reverse('adicionar_apostilas')
        response = self.client.get(url)

        self.assertEqual(
            response.context['views_totais'],
            query_for_test
        )

    def test_adicionar_apostila_view_method_post_return_status_code_200(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('adicionar_apostilas')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

    def test_adicionar_apostila_view_method_post_use_right_template(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('adicionar_apostilas')
        response = self.client.post(url)

        self.assertTemplateUsed(response, 'adicionar_apostilas.html')

    def test_adicionar_apostila_view_method_post_return_apostilas_in_context(self):  # noqa:E501
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('adicionar_apostilas')
        response = self.client.post(url)

        self.assertIn('apostilas', response.context)

    def test_adicionar_apostila_view_method_post_return_views_totais_in_context(self):  # noqa:E501
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('adicionar_apostilas')
        response = self.client.post(url)

        self.assertIn('views_totais', response.context)

    def test_adicionar_apostila_view_method_post_return_apostila_tag_in_context(self):  # noqa:E501
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        url = reverse('adicionar_apostilas')
        response = self.client.post(url)

        self.assertIn('apostila_tag', response.context)

    def test_adicionar_apostila_view_method_post_the_content_of_context_apostilas_is_right(self):  # noqa:E501
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        query_for_test = Apostila.objects.filter(user=user)

        url = reverse('adicionar_apostilas')
        response = self.client.post(url)

        self.assertEqual(
            response.context['apostilas'].first(),
            query_for_test.first()
        )

    def test_adicionar_apostila_view_method_post_the_content_of_context_views_totais_is_right(self):  # noqa:E501
        view_apostila = self.make_view_apostila()
        user = view_apostila.apostila.user
        self.client.force_login(user)

        query_for_test = (
            ViewApostila.objects.filter(apostila__user=user).count()
        )

        url = reverse('adicionar_apostilas')
        response = self.client.post(url)

        self.assertEqual(
            response.context['views_totais'],
            query_for_test
        )

    def test_adicionar_apostila_view_method_post_the_content_of_context_apostila_tag_is_right(self):  # noqa:E501
        view_apostila = self.make_view_apostila()
        user = view_apostila.apostila.user
        self.client.force_login(user)

        query_for_test = (
            Apostila.objects.filter(titulo__icontains='')
        )

        url = reverse('adicionar_apostilas')
        response = self.client.post(url)

        self.assertEqual(
            response.context['apostila_tag'].first(),
            query_for_test.first()
        )

    def test_adicionar_apostila_view_method_post_find_apostila(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        search = {
            'tags': 'apostila'
        }

        url = reverse('adicionar_apostilas')
        response = self.client.post(url, data=search)

        self.assertEqual(
            response.context['apostilas'].first().titulo,
            'apostila test'
        )
        self.assertIn(
            'Apostilas filtradas com sucesso!',
            response.content.decode('utf-8')
        )

    def test_adicionar_apostila_view_method_post_dont_find_apostila(self):
        apostila = self.make_apostila()
        user = apostila.user
        self.client.force_login(user)

        search = {
            'tags': 'Ola'
        }

        url = reverse('adicionar_apostilas')
        response = self.client.post(url, data=search, follow=True)

        self.assertIn(
            'Nenhuma apostila encontrada com as tags fornecidas.',
            response.content.decode('utf-8')
        )

    def test_adicionar_apostila_create_new_apostila(self):
        apostila = self.make_apostila()
        arquivo = apostila.arquivo
        user = apostila.user
        self.client.force_login(user)

        data = {
            'user': user,
            'titulo': apostila.titulo,
            'arquivo': arquivo
        }

        url = reverse('adicionar_apostilas')
        response = self.client.post(url, data=data)

        self.assertIn(
            'Apostila salva com sucesso!',
            response.content.decode('utf-8')
        )
