from apostilas.tests.test_base import (
    BaseTestMixin, Categoria, Flashcard, Desafio
)
from flashcard import views

from django.urls import reverse, resolve


class IniciarDesafioViewTest(BaseTestMixin):

    # METHOD GET
    def test_iniciar_desafio_view_is_correct(self):
        view = resolve(reverse('iniciar_desafio'))

        self.assertIs(view.func.view_class, views.IniciarDesafioView)

    def test_iniciar_desafio_view_method_get_status_code_200(self):
        user = self.get_user()
        self.client.force_login(user)

        url = reverse('iniciar_desafio')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_iniciar_desafio_view_method_get_uses_right_template(self):
        user = self.get_user()
        self.client.force_login(user)

        url = reverse('iniciar_desafio')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'iniciar_desafio.html')

    def test_iniciar_desafio_view_method_get_have_categorias_in_context(self):
        user = self.get_user()
        self.client.force_login(user)

        url = reverse('iniciar_desafio')
        response = self.client.get(url)

        self.assertIn('categorias', response.context)

    def test_iniciar_desafio_view_method_get_have_dificuldades_in_context(self):  # noqa:E501
        user = self.get_user()
        self.client.force_login(user)

        url = reverse('iniciar_desafio')
        response = self.client.get(url)

        self.assertIn('dificuldades', response.context)

    def test_iniciar_desafio_view_method_get_categorias_context_have_the_right_content(self):  # noqa:E501
        self.make_categoria()
        user = self.get_user()
        self.client.force_login(user)

        categoria = Categoria.objects.all()

        url = reverse('iniciar_desafio')
        response = self.client.get(url)

        print(response.context)

        self.assertEqual(
            categoria.first(), response.context['categorias'].first()
        )

    def test_iniciar_desafio_view_method_get_dificuldades_context_have_the_right_content(self):  # noqa:E501
        user = self.get_user()
        self.client.force_login(user)

        flashcard_dificuldade = Flashcard.DIFICULDADE_CHOICES

        url = reverse('iniciar_desafio')
        response = self.client.get(url)

        self.assertEqual(
            flashcard_dificuldade, response.context['dificuldades']
        )

    # METHOD POST
    def test_iniciar_desafio_view_method_post_create_new_desafio(self):
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        categoria = self.make_categoria()

        flashcard_dois = Flashcard.objects.create(
            user=user,
            pergunta='Test 2?',
            resposta='yes test2',
            categoria=categoria,
            dificuldade='M',
        )
        flashcard_dois.save()

        desafio_data = {
            'titulo': 'new test desafio',
            'categoria': [categoria.id,],
            'dificuldade': 'M',
            'qtd_perguntas': 1
        }

        url = reverse('iniciar_desafio')
        self.client.post(url, data=desafio_data)

        self.assertTrue(
            Desafio.objects.filter(
                titulo='new test desafio').exists()
        )

    def test_iniciar_desafio_view_method_post_qtd_perguntas_gt_flashcards_count_and_redirect(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        categoria = self.make_categoria()

        desafio_data = {
            'titulo': 'new test desafio',
            'categoria': [categoria.id,],
            'dificuldade': 'M',
            'qtd_perguntas': 3
        }

        url = reverse('iniciar_desafio')
        response = self.client.post(url, data=desafio_data)

        self.assertEqual(response.status_code, 302)

    def test_iniciar_desafio_view_method_post_qtd_perguntas_gt_flashcards_count_and_redirect_to_right_link(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        categoria = self.make_categoria()

        desafio_data = {
            'titulo': 'new test desafio',
            'categoria': [categoria.id,],
            'dificuldade': 'M',
            'qtd_perguntas': 3
        }

        url = reverse('iniciar_desafio')
        response = self.client.post(url, data=desafio_data, follow=True)

        self.assertRedirects(response, '/flashcard/iniciar_desafio/')
