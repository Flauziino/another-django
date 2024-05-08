from django.test import TestCase
from django.urls import reverse


class ApostilasURLsTest(TestCase):

    def test_adicionar_apostilas_urls_is_correct(self):
        url = reverse('adicionar_apostilas')
        self.assertEqual(
            url, '/apostilas/adicionar_apostilas/'
        )

    def test_apostila_urls_is_correct(self):
        url = reverse('apostila', kwargs={'id': 1})
        self.assertEqual(
            url, '/apostilas/apostila/1'
        )
