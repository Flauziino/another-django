from apostilas.tests.test_base import (BaseTestMixin, User)
from flashcard import views

from django.urls import reverse, resolve


class DesafioViewTest(BaseTestMixin):

    def test_desafio_view_is_correct(self):
        view = resolve(reverse('desafio', kwargs={'id': 1}))

        self.assertIs(view.func, views.desafio)

    def test_desafio_view_view_find_desafio_with_same_user_status_code_200(self):  # noqa:E501
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_desafio_view_view_dont_find_desafio_from_user_status_code_404(self):  # noqa:E501
        desafio = self.make_desafio()

        user = User.objects.create_user(
            username='user?',
            password='password'
        )
        self.client.force_login(user)

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_desafio_view_uses_the_right_template(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'desafio.html')

    def test_desafio_view_have_desafio_in_context(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertIn('desafio', response.context)

    def test_desafio_view_have_acertos_in_context(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertIn('acertos', response.context)

    def test_desafio_view_have_erros_in_context(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertIn('erros', response.context)

    def test_desafio_view_have_faltantes_in_context(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertIn('faltantes', response.context)

    def test_desafio_view_desafio_context_is_right(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(response.context['desafio'], desafio)

    def test_desafio_view_faltantes_context_is_right(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(response.context['faltantes'], 1)

    def test_desafio_view_acertos_context_is_right(self):
        desafio = self.make_desafio()

        for flashcard_desafio in desafio.flashcards.all():
            flashcard_desafio.respondido = True
            flashcard_desafio.acertou = True
            flashcard_desafio.save()

        user = desafio.user
        self.client.force_login(user)

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(response.context['acertos'], 1)

    def test_desafio_view_erros_context_is_right(self):
        desafio = self.make_desafio()

        for flashcard_desafio in desafio.flashcards.all():
            flashcard_desafio.respondido = True
            flashcard_desafio.acertou = False
            flashcard_desafio.save()

        user = desafio.user
        self.client.force_login(user)

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(response.context['erros'], 1)

    def test_desafio_view_acertos_and_erros_context_is_right(self):
        desafio = self.make_desafio()

        for flashcard_desafio in desafio.flashcards.all():
            flashcard_desafio.respondido = True
            flashcard_desafio.acertou = True
            flashcard_desafio.save()

        user = desafio.user
        self.client.force_login(user)

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(response.context['acertos'], 1)
        self.assertEqual(response.context['erros'], 0)

        for flashcard_desafio in desafio.flashcards.all():
            flashcard_desafio.respondido = True
            flashcard_desafio.acertou = False
            flashcard_desafio.save()

        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(response.context['acertos'], 0)
        self.assertEqual(response.context['erros'], 1)
