from apostilas.tests.test_base import (BaseTestMixin, User)
from flashcard import views

from django.urls import reverse, resolve


class ResponderFlashcardViewTest(BaseTestMixin):

    def test_responder_flashcard_view_is_correct(self):
        view = resolve(reverse('responder_flashcard', kwargs={'id': 1}))

        self.assertIs(view.func.view_class, views.ResponderFlashcardView)

    def test_responder_flashcard_view_redirect_status_code_302(self):
        flashcard_desafio = self.make_flashcard_desafio()
        user = flashcard_desafio.flashcard.user
        self.client.force_login(user)

        url = reverse(
            'responder_flashcard',
            kwargs={'id': flashcard_desafio.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_responder_flashcard_view_status_404_with_wrong_user(self):
        flashcard_desafio = self.make_flashcard_desafio()

        user = User.objects.create_user(
            username='fdesafio',
            password='fd1234'
        )
        user.save()
        self.client.force_login(user)

        url = reverse(
            'responder_flashcard',
            kwargs={'id': flashcard_desafio.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_responder_flashcard_view_is_all_correct(self):
        # criando um desafio
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        # testando inicialmente a view desafio, com faltantes = 1
        # pois respondido esta como False
        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(response.context['faltantes'], 1)

        # pegando apenas um flashcard_desafio para testar o funcionamento
        # da view flash_card_desafio
        # espera-se que ela mude o respondido de False (padrao), para True
        flash_d = desafio.flashcards.all().first()
        url = reverse(
            'responder_flashcard',
            kwargs={'id': flash_d.id}
        )

        # ativando a view flashcard_desafio, ela vai renderizar de volta para
        # view desafio.
        self.client.get(url, follow=True)

        # agora entrando de fato na view desafio pra ver se o
        # respondido passou para True, e mudou faltantes de 1 pra 0
        # e o erro de 0 para 1, ja que nao foi testado acerto.
        url = reverse('desafio', kwargs={'id': desafio.id})
        response = self.client.get(url)

        self.assertEqual(response.context['erros'], 1)
