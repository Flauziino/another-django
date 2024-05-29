from apostilas.tests.test_base import BaseTestMixin
from flashcard import views

from django.urls import reverse, resolve


class RelatorioViewTest(BaseTestMixin):

    def test_relatorio_view_is_correct(self):
        view = resolve(reverse('relatorio', kwargs={'id': 1}))

        self.assertIs(view.func.view_class, views.RelatorioView)

    def test_relatorio_view_status_code_200_if_find_desafio(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('relatorio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_relatorio_view_uses_right_template(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('relatorio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'relatorio.html')

    def test_relatorio_view_have_dasafio_in_context(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('relatorio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertIn('desafio', response.context)

    def test_relatorio_view_have_dados_in_context(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('relatorio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertIn('dados', response.context)

    def test_relatorio_view_have_categorias_in_context(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('relatorio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertIn('categorias', response.context)

    def test_relatorio_view_have_dados2_in_context(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('relatorio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertIn('dados2', response.context)

    def test_relatorio_view_have_melhores_in_context(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('relatorio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertIn('melhores', response.context)

    def test_relatorio_view_have_piores_in_context(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('relatorio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertIn('piores', response.context)

    def test_relatorio_view_total_flashcards_equal_zero(self):
        desafio = self.make_desafio_without_flash()

        user = desafio.user
        self.client.force_login(user)

        url = reverse('relatorio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_relatorio_view_proporcao_acerto_gt_0_5(self):
        desafio = self.make_desafio()

        for flashcard_desafio in desafio.flashcards.all():
            flashcard_desafio.respondido = True
            flashcard_desafio.acertou = True
            flashcard_desafio.save()

        user = desafio.user
        self.client.force_login(user)

        url = reverse('relatorio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(
            response.context['melhores'][0]['proporcao_acertos'],
            1
        )
