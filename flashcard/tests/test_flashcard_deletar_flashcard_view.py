from apostilas.tests.test_base import BaseTestMixin, User
from flashcard import views

from django.urls import reverse, resolve


class DeletarFlashcardViewTest(BaseTestMixin):
    def test_deletar_flashcard_view_is_correct(self):
        view = resolve(reverse('deletar_flashcard', kwargs={'id': 1}))

        self.assertIs(view.func, views.deletar_flashcard)

    def test_deletar_flashcard_view_return_status_code_302_if_find_flashcard_and_delete(self):  # noqa:E501
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        url = reverse('deletar_flashcard', kwargs={'id': flashcard.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_deletar_flashcard_view_contain_success_message(self):
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        url = reverse('deletar_flashcard', kwargs={'id': flashcard.id})
        response = self.client.get(url, follow=True)

        self.assertIn(
            'Flashcard deletado com sucesso!',
            response.content.decode('utf-8')
        )

    def test_deletar_flashcard_view_redirect_to_right_link(self):
        flashcard = self.make_flashcard()
        user = flashcard.user
        self.client.force_login(user)

        url = reverse('deletar_flashcard', kwargs={'id': flashcard.id})
        response = self.client.get(url, follow=True)

        self.assertRedirects(response, '/flashcard/novo_flashcard/')

    def test_deletar_flashcard_view_fail_to_delete_if_not_the_flashcard_owner_and_redirects(self):  # noqa:E501
        flashcard = self.make_flashcard()

        user = User.objects.create_user(
            username='fail_user',
            password='123456'
        )
        user.save()
        self.client.force_login(user)

        url = reverse('deletar_flashcard', kwargs={'id': flashcard.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_deletar_flashcard_view_fail_to_delete_if_not_the_flashcard_owner_contain_the_error_msg(self):  # noqa:E501
        flashcard = self.make_flashcard()

        user = User.objects.create_user(
            username='fail_user',
            password='123456'
        )
        user.save()
        self.client.force_login(user)

        url = reverse('deletar_flashcard', kwargs={'id': flashcard.id})
        response = self.client.get(url, follow=True)

        self.assertIn(
            'Voce nao pode deletar esse flashcard!',
            response.content.decode('utf-8')
        )

    def test_deletar_flashcard_view_fail_to_delete_if_not_the_flashcard_owner_and_redirect_to_right_link(self):  # noqa:E501
        flashcard = self.make_flashcard()

        user = User.objects.create_user(
            username='fail_user',
            password='123456'
        )
        user.save()
        self.client.force_login(user)

        url = reverse('deletar_flashcard', kwargs={'id': flashcard.id})
        response = self.client.get(url, follow=True)

        self.assertRedirects(response, '/flashcard/novo_flashcard/')
