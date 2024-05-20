from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


from apostilas.models import Apostila, Avaliacao, ViewApostila
from flashcard.models import (
    Categoria, Flashcard, FlashcardDesafio, Desafio
)


class BaseTestMixin(TestCase):
    def get_user(self, username='test', password='123456'):
        user = User.objects.create_user(
            username=username,
            password=password
        )
        user.save()
        return user

    def make_apostila(self):
        user = self.get_user()
        file_content = b'test test'
        arquivo = SimpleUploadedFile("arquivo.txt", file_content)

        apostila = Apostila.objects.create(
            user=user,
            titulo='apostila test',
            arquivo=arquivo

        )
        apostila.save()
        return apostila

    def make_view_apostila(self):
        apostila = self.make_apostila()

        view_apostila = ViewApostila.objects.create(
            ip='192.0.2.0',
            apostila=apostila
        )
        view_apostila.save()
        return view_apostila

    def make_avaliacao(self):
        avaliacao = Avaliacao.objects.create(
            avaliacao='bom'
        )
        avaliacao.save()
        return avaliacao

    def make_categoria(self):
        categoria = Categoria.objects.create(nome='Cat test')
        categoria.save()
        return categoria

    def make_flashcard(self):
        categoria = self.make_categoria()
        user = self.get_user()
        flashcard = Flashcard.objects.create(
            user=user,
            pergunta='Test?',
            resposta='yes test',
            categoria=categoria,
            dificuldade='M',
        )
        flashcard.save()
        return flashcard

    def make_flashcard_desafio(self):
        flashcard = self.make_flashcard()
        flashcard_desafio = FlashcardDesafio.objects.create(
            flashcard=flashcard,
        )
        flashcard_desafio.save()
        return flashcard_desafio

    def make_desafio(self):
        fashcard_desafio = self.make_flashcard_desafio()
        desafio = Desafio.objects.create(
            user=fashcard_desafio.flashcard.user,
            titulo='test desafio',
            quantidade_perguntas=1,
            dificuldade='M',
        )
        desafio.categoria.set([fashcard_desafio.flashcard.categoria])
        desafio.flashcards.set([fashcard_desafio])
        desafio.save()
        return desafio

    def make_desafio_without_flash(self):
        user = self.get_user()
        categoria = self.make_categoria()
        desafio = Desafio.objects.create(
            user=user,
            titulo='test desafio',
            quantidade_perguntas=1,
            dificuldade='M',
        )
        desafio.categoria.set([categoria])
        return desafio
