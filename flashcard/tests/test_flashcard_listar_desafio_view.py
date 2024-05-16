from apostilas.tests.test_base import (
    BaseTestMixin, Flashcard, Categoria, User
)
from flashcard import views

from django.urls import reverse, resolve


class ListarDesafioViewTest(BaseTestMixin):

    def test_listar_desafio_view_is_correct(self):
        view = resolve(reverse('listar_desafio'))

        self.assertIs(view.func, views.listar_desafio)

    def test_listar_desafio_view_with_auth_user_status_code_200_if_find_desafio(self):  # noqa:E501
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('listar_desafio')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_listar_desafio_view_with_auth_user_uses_right_template(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('listar_desafio')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'listar_desafio.html')

    def test_listar_desafio_view_with_auth_user_have_desafios_in_context(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('listar_desafio')
        response = self.client.get(url)

        self.assertIn('desafios', response.context)

    def test_listar_desafio_view_with_auth_user_have_status_in_context(self):
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('listar_desafio')
        response = self.client.get(url)

        self.assertIn('status', response.context)

    def test_listar_desafio_view_with_auth_user_have_categorias_in_context(self):  # noqa: E501
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('listar_desafio')
        response = self.client.get(url)

        self.assertIn('categorias', response.context)

    def test_listar_desafio_view_with_auth_user_have_dificuldades_in_context(self):  # noqa: E501
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('listar_desafio')
        response = self.client.get(url)

        self.assertIn('dificuldades', response.context)

    def test_listar_desafio_view_with_auth_user_receive_correct_categoria_and_dificuldade(self):  # noqa:E501
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('listar_desafio') + '?categoria=1&dificuldade=M'
        response = self.client.get(url)

        desafio_check = response.context['desafios'].first()

        self.assertEqual(
            desafio.dificuldade,
            desafio_check.dificuldade
        )
        self.assertEqual(
            desafio.categoria,
            desafio_check.categoria
        )

    def test_listar_desafio_view_with_auth_user_receive_wrong_categoria_and_dificuldade(self):  # noqa:E501
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        # passando categoria e dificuldades que nao existem
        url = reverse('listar_desafio') + '?categoria=999&dificuldade=A'
        response = self.client.get(url)

        # Espera-se que esse contexto seja None, pois a categoria
        # e a dificuldade não existem, por conta disso na hora de filtrar
        # pela logica da funcao, nao vai ser retornado nada
        desafio_check = response.context['desafios'].first()

        # checando se de fato esta none
        self.assertIsNone(desafio_check)

    def test_listar_desafio_view_with_auth_user_have_dificuldades_in_context_is_right(self):  # noqa: E501
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('listar_desafio')
        response = self.client.get(url)

        dificuldades = Flashcard.DIFICULDADE_CHOICES

        self.assertEqual(
            response.context['dificuldades'],
            dificuldades
        )

    def test_listar_desafio_view_with_auth_user_have_categorias_in_context_is_right(self):  # noqa: E501
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('listar_desafio')
        response = self.client.get(url)

        categorias = Categoria.objects.all()

        self.assertEqual(
            response.context['categorias'].first(),
            categorias.first()
        )

    def test_listar_desafio_view_with_auth_user_have_status_in_context_is_right(self):  # noqa: E501
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('listar_desafio')
        response = self.client.get(url)

        self.assertEqual(
            response.context['status'].first(),
            desafio.flashcards.first()
        )

    def test_listar_desafio_view_with_auth_user_have_desafios_in_context_is_right(self):  # noqa: E501
        desafio = self.make_desafio()
        user = desafio.user
        self.client.force_login(user)

        url = reverse('listar_desafio')
        response = self.client.get(url)

        self.assertEqual(
            response.context['desafios'].first(),
            desafio
        )

    def test_listar_desafio_view_with_auth_user_have_desafios_in_context_is_a_empty_query_with_another_user(self):  # noqa: E501
        self.make_desafio()

        user = User.objects.create_user(
            username='For Now',
            password='12345'
        )
        user.save()
        self.client.force_login(user)

        url = reverse('listar_desafio')
        response = self.client.get(url)

        self.assertQuerySetEqual(response.context['desafios'], [])
