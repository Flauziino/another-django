from apostilas.tests.test_base import BaseTestMixin, Categoria, Flashcard
from flashcard import views

from django.urls import reverse, resolve


class NovoFlashcardViewTest(BaseTestMixin):

    # METHOD GET
    def test_novo_flashcard_view_is_correct(self):
        view = resolve(reverse('novo_flashcard'))

        self.assertIs(view.func.view_class, views.NovoFlashcard)

    def test_novo_flashcard_view_status_code_302_if_not_auth_user(self):
        url = reverse('novo_flashcard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_novo_flashcard_view_redirect_to_right_page_without_auth_user(self):  # noqa: E501
        url = reverse('novo_flashcard')
        response = self.client.get(url, follow=True)

        self.assertRedirects(
            response,
            '/usuarios/logar/?next=/flashcard/novo_flashcard/'
        )

    def test_novo_flashcard_view_with_auth_user_method_get_status_code_200(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        url = reverse('novo_flashcard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_novo_flashcard_view_with_auth_user_method_get_use_right_template(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        url = reverse('novo_flashcard')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'novo_flashcard.html')

    def test_novo_flashcard_view_with_auth_user_method_get_have_categoria_in_context(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        url = reverse('novo_flashcard')
        response = self.client.get(url)

        self.assertIn('categoria', response.context)

    def test_novo_flashcard_view_with_auth_user_method_get_have_dificuldade_in_context(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        url = reverse('novo_flashcard')
        response = self.client.get(url)

        self.assertIn('dificuldade', response.context)

    def test_novo_flashcard_view_with_auth_user_method_get_have_flashcards_in_context(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        url = reverse('novo_flashcard')
        response = self.client.get(url)

        self.assertIn('flashcards', response.context)

    def test_novo_flashcard_view_with_auth_user_method_get_have_categoria_and_dificuldade(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        categoria = Categoria.objects.all().first()
        flashcard_test = Flashcard.objects.all()
        flashcard_test_dificuldade = Flashcard.DIFICULDADE_CHOICES

        url = reverse('novo_flashcard') + '?categoria=1&dificuldade=M'
        response = self.client.get(url)

        self.assertEqual(
            flashcard_test_dificuldade,
            response.context['dificuldade']
        )
        self.assertEqual(
            response.context['categoria'].first(),
            categoria
        )
        self.assertEqual(
            response.context['flashcards'].first(),
            flashcard_test.first()
        )

    # METHOD POST
    def test_novo_flashcard_view_without_auth_user_method_post_will_redirect_status_code_302(self):  # noqa:E501
        url = reverse('novo_flashcard')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

    def test_novo_flashcard_view_without_auth_user_method_post_will_redirect_to_right_page(self):  # noqa:E501
        url = reverse('novo_flashcard')
        response = self.client.post(url, follow=True)

        self.assertRedirects(
            response,
            '/usuarios/logar/?next=/flashcard/novo_flashcard/'
        )

    def test_novo_flashcard_view_with_auth_user_method_post_without_pergunta_redirects(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        flashcard_data = {
            'pergunta': '',
            'resposta': 'oi ?',
            'categoria': '1',
            'dificuldade': 'M'
        }

        url = reverse('novo_flashcard')
        response = self.client.post(
            url,
            data=flashcard_data,
            follow=True)

        self.assertRedirects(response, '/flashcard/novo_flashcard/')

    def test_novo_flashcard_view_with_auth_user_method_post_without_resposta_redirects(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        flashcard_data = {
            'pergunta': 'OI ?',
            'resposta': '',
            'categoria': '1',
            'dificuldade': 'M'
        }

        url = reverse('novo_flashcard')
        response = self.client.post(
            url,
            data=flashcard_data,
            follow=True)

        self.assertRedirects(response, '/flashcard/novo_flashcard/')

    def test_novo_flashcard_view_with_auth_user_method_post_without_pergunta_or_resposta_have_the_error_msg(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        flashcard_data = {
            'pergunta': '',
            'resposta': '',
            'categoria': '1',
            'dificuldade': 'M'
        }

        url = reverse('novo_flashcard')
        response = self.client.post(
            url,
            data=flashcard_data,
            follow=True)

        self.assertIn(
            'Preencha os campos de pergunta e resposta',
            response.content.decode('utf-8')
        )

    def test_novo_flashcard_view_with_auth_user_method_post_succes_on_create_new_flashcard(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        flashcard_data = {
            'pergunta': 'Test ???',
            'resposta': 'Test!!!',
            'categoria': '1',
            'dificuldade': 'F'
        }

        url = reverse('novo_flashcard')
        response = self.client.post(
            url,
            data=flashcard_data,
            follow=True)

        novo_flashcard = Flashcard.objects.filter(pergunta='Test ???')

        self.assertRedirects(response, '/flashcard/novo_flashcard/')
        self.assertIn(
            'Flashcard criado com sucesso',
            response.content.decode('utf-8')
        )
        self.assertTrue(novo_flashcard.exists())
