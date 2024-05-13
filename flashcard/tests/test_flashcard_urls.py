from django.test import TestCase
from django.urls import reverse


class FlashcardURLsTest(TestCase):

    def test_novo_flashcard_urls_is_correct(self):
        url = reverse('novo_flashcard')
        self.assertEqual(url, '/flashcard/novo_flashcard/')

    def test_deletar_flashcard_urls_is_correct(self):
        url = reverse('deletar_flashcard', kwargs={'id': 1})
        self.assertEqual(url, '/flashcard/deletar_flashcard/1')

    def test_iniciar_desafio_urls_is_correct(self):
        url = reverse('iniciar_desafio')
        self.assertEqual(url, '/flashcard/iniciar_desafio/')

    def test_listar_desafio_urls_is_correct(self):
        url = reverse('listar_desafio')
        self.assertEqual(url, '/flashcard/listar_desafio/')

    def test_desafio_urls_is_correct(self):
        url = reverse('desafio', kwargs={'id': 1})
        self.assertEqual(url, '/flashcard/desafio/1/')

    def test_responder_flashcard_urls_is_correct(self):
        url = reverse('responder_flashcard', kwargs={'id': 1})
        self.assertEqual(url, '/flashcard/responder_flashcard/1/')

    def test_relatorio_urls_is_correct(self):
        url = reverse('relatorio', kwargs={'id': 1})
        self.assertEqual(url, '/flashcard/relatorio/1/')
