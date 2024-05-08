from django.core.exceptions import ValidationError

from apostilas.tests.test_base import BaseTestMixin


class ApostilaTestModels(BaseTestMixin):
    # ////////////////////////
    # testes do model Apostila
    def test_apostila_apostila_model_str_representation(self):
        apostila = self.make_apostila()
        self.assertEqual(
            str(apostila), apostila.titulo
        )

    def test_apostila_apostila_model_titulo_field_max_length_need_to_be_lt_100_chars(self):  # noqa: E501
        apostila = self.make_apostila()
        apostila.titulo = 'A' * 200

        with self.assertRaises(ValidationError):
            apostila.full_clean()

    # ////////////////////////////
    # testes do model ViewApostila
    def test_apostila_view_apostila_model_str_representation(self):
        view_apostila = self.make_view_apostila()
        self.assertEqual(
            str(view_apostila), view_apostila.ip
        )

    # /////////////////////////
    # testes do model Avaliacao
    def test_apostila_avaliacao_model_str_representation(self):
        avaliacao = self.make_avaliacao()
        self.assertEqual(
            str(avaliacao), avaliacao.avaliacao
        )

    def test_apostila_avaliacao_model_save_correct_avaliacao(self):
        avaliacao = self.make_avaliacao()
        # testando se esta salvando a avaliacao correta
        # espera-se que esteja como 'bom' pois é o padrao criado na base de
        # testes
        self.assertEqual(avaliacao.avaliacao, 'bom')

    def test_apostila_avaliacao_model_avaliacao_field_max_length_need_to_be_lt_10_char(self):  # noqa:E501
        avaliacao = self.make_avaliacao()
        self.assertEqual(
            avaliacao._meta.get_field('avaliacao').max_length,
            10
        )
