from django.core.exceptions import ValidationError

from apostilas.tests.test_base import (
    BaseTestMixin, User, Flashcard, Categoria, FlashcardDesafio
)


class FlashcardModelsTest(BaseTestMixin):
    # MODEL CATEGORIA
    # ///////////////
    def test_flashcard_model_categoria_str_representation(self):
        categoria = self.make_categoria()
        self.assertEqual(
            str(categoria), categoria.nome
        )

    def test_flashcard_model_categoria_field_nome_max_length_need_to_be_lt_20_chars(self):  # noqa:E501
        categoria = self.make_categoria()
        categoria.nome = 'A' * 25

        with self.assertRaises(ValidationError):
            categoria.full_clean()

    # MODEL FLASHCARD
    # ///////////////
    def test_flashcard_model_flashcard_str_representation(self):
        flashcard = self.make_flashcard()
        self.assertEqual(
            str(flashcard), flashcard.pergunta
        )

    def test_flashcard_model_flashcard_user_field_is_correct(self):
        flashcard = self.make_flashcard()
        user = User.objects.all()

        self.assertEqual(flashcard.user, user.first())

    def test_flashcard_model_flashcard_pergunta_field_max_length_need_to_be_lt_100_chars(self):  # noqa: E501
        flashcard = self.make_flashcard()
        flashcard.pergunta = 'A' * 105

        with self.assertRaises(ValidationError):
            flashcard.full_clean()

    def test_flashcard_model_flashcard_method_css_dificuldade_return_the_right_value_for_F_difficult(self):  # noqa: E501
        flashcard = self.make_flashcard()
        flashcard.dificuldade = 'F'
        flashcard.save()
        self.assertEqual(flashcard.css_dificuldade, 'flashcard-facil')

    def test_flashcard_model_flashcard_method_css_dificuldade_return_the_right_value_for_D_difficult(self):  # noqa: E501
        flashcard = self.make_flashcard()
        flashcard.dificuldade = 'D'
        flashcard.save()
        self.assertEqual(flashcard.css_dificuldade, 'flashcard-dificil')

    def test_flashcard_model_flashcard_method_css_dificuldade_return_the_right_value_for_M_difficult(self):  # noqa: E501
        flashcard = self.make_flashcard()
        self.assertEqual(flashcard.css_dificuldade, 'flashcard-medio')

    def test_flashcard_model_flashcard_method_css_dificuldade_return_the_right_value_for_wrong_difficult(self):  # noqa: E501
        flashcard = self.make_flashcard()
        flashcard.dificuldade = 'A'
        flashcard.save()
        self.assertEqual(
            flashcard.css_dificuldade,
            'dificuldade-nao-encontrada'
        )

    # MODEL FLASHCARDDESAFIO
    # //////////////////////
    def test_flashcard_model_flashcard_desafio_str_representation(self):
        flashcard_desafio = self.make_flashcard_desafio()
        self.assertEqual(
            str(flashcard_desafio), flashcard_desafio.flashcard.pergunta
        )

    def test_flashcard_model_flashcard_desafio_flashcard_field_is_correct(self):  # noqa: E501
        flashcard_desafio = self.make_flashcard_desafio()
        flashcard = Flashcard.objects.all().first()
        self.assertEqual(
            flashcard_desafio.flashcard,
            flashcard
        )

    def test_flashcard_model_flashcard_desafio_respondido_field_is_false_by_default(self):  # noqa: E501
        flashcard_desafio = self.make_flashcard_desafio()
        self.assertEqual(flashcard_desafio.respondido, False)

    def test_flashcard_model_flashcard_desafio_acertou_field_is_false_by_default(self):  # noqa: E501
        flashcard_desafio = self.make_flashcard_desafio()
        self.assertEqual(flashcard_desafio.acertou, False)

    # MODEL DESAFIO
    # /////////////
    def test_flashcard_model_desafio_str_representation(self):
        desafio = self.make_desafio()
        self.assertEqual(
            str(desafio), desafio.titulo
        )

    def test_flashcard_model_desafio_titulo_field_max_length_need_to_be_lt_100_chars(self):  # noqa:E501
        desafio = self.make_desafio()
        desafio.titulo = 'A' * 105

        with self.assertRaises(ValidationError):
            desafio.full_clean()

    def test_flashcard_model_desafio_user_field_is_correct(self):
        desafio = self.make_desafio()
        user = User.objects.all().first()

        self.assertEqual(desafio.user, user)

    def test_flashcard_model_desafio_categoria_field_is_correct(self):
        desafio = self.make_desafio()
        categoria = Categoria.objects.all()

        self.assertEqual(desafio.categoria.first(), categoria.first())

    def test_flashcard_model_desafio_flashcards_field_is_correct(self):
        desafio = self.make_desafio()
        flashcard_desafio = FlashcardDesafio.objects.all()

        self.assertEqual(
            desafio.flashcards.first(),
            flashcard_desafio.first()
        )
