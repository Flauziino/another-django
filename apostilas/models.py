from django.db import models
from django.contrib.auth.models import User


class Apostila(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='apostilas')

    def __str__(self):
        return self.titulo


class ViewApostila(models.Model):
    ip = models.GenericIPAddressField()
    apostila = models.ForeignKey(Apostila, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.ip


class Avaliacao(models.Model):
    AVALIACAO_CHOICES = [
        ('ruim', 'Ruim'),
        ('bom', 'Bom'),
        ('otimo', 'Otimo'),
    ]

    avaliacao = models.CharField(max_length=10, choices=AVALIACAO_CHOICES)

    def __str__(self):
        return self.avaliacao
