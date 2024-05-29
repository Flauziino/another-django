from .models import Apostila, ViewApostila, Avaliacao

from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from django.views import View


class AdicionarApostilasView(View):
    def get_render(self, apostilas=None, views_totais=None, apostila_tag=None):
        ctx = {
            'apostilas': apostilas,
            'views_totais': views_totais,
            'apostila_tag': apostila_tag
        }

        return render(
            self.request,
            'adicionar_apostilas.html',
            ctx
        )

    def get(self, request):
        apostilas = Apostila.objects.filter(user=request.user)
        views_totais = (
            ViewApostila.objects.filter(apostila__user=request.user)
            .count()
        )

        return self.get_render(
            apostilas,
            views_totais
        )

    def post(self, request):
        busca = request.POST.get('tags', '')
        apostilas = Apostila.objects.filter(user=request.user)
        views_totais = (
            ViewApostila.objects.filter(apostila__user=request.user)
            .count()
        )
        apostila_tag = Apostila.objects.filter(titulo__icontains=busca)

        if 'arquivo' in request.FILES:
            titulo = request.POST.get('titulo')
            arquivo = request.FILES['arquivo']

            apostila = Apostila(
                user=request.user,
                titulo=titulo,
                arquivo=arquivo
            )
            apostila.save()

            messages.add_message(
                request,
                constants.SUCCESS,
                'Apostila salva com sucesso!'
            )

        if apostila_tag.exists():
            messages.add_message(
                request,
                constants.SUCCESS,
                'Apostilas filtradas com sucesso!'
            )

        else:
            messages.add_message(
                request,
                constants.INFO,
                'Nenhuma apostila encontrada com as tags fornecidas.'
            )

            return redirect(
                'adicionar_apostilas'
            )

        return self.get_render(
            apostilas,
            views_totais,
            apostila_tag
        )


class ApostilaView(View):
    def post(self, request, id):
        avaliacao = request.POST.get('avaliacao')

        if avaliacao in ['ruim', 'bom', 'otimo']:
            Avaliacao.objects.create(avaliacao=avaliacao)

            return redirect('apostila', id=id)

    def get(self, request, id):
        apostila = Apostila.objects.get(id=id)
        total_avaliacoes = Avaliacao.objects.count()

        avaliacoes_ruim = Avaliacao.objects.filter(avaliacao='ruim').count()
        proporcao_ruim = (
            avaliacoes_ruim / total_avaliacoes if total_avaliacoes > 0 else 0
        )

        avaliacoes_bom = Avaliacao.objects.filter(avaliacao='bom').count()
        proporcao_bom = (
            avaliacoes_bom / total_avaliacoes if total_avaliacoes > 0 else 0
        )

        avaliacoes_otimo = Avaliacao.objects.filter(avaliacao='otimo').count()
        proporcao_otimo = (
            avaliacoes_otimo / total_avaliacoes if total_avaliacoes > 0 else 0
        )

        # Encontrar a avaliação com a maior proporção
        proporcoes = {
            'ruim': proporcao_ruim,
            'bom': proporcao_bom,
            'otimo': proporcao_otimo
        }
        maior_avaliacao = max(proporcoes, key=proporcoes.get)

        view = ViewApostila(
            ip=request.META['REMOTE_ADDR'],
            apostila=apostila
        )
        view.save()

        views_unicas = (
            ViewApostila.objects.filter(apostila=apostila)
            .values('ip')
            .distinct()
            .count()
        )
        views_totais = (
            ViewApostila.objects.filter(apostila=apostila)
            .count()
        )

        return render(
            request,
            'apostila.html',
            {
                'apostila': apostila,
                'views_unicas': views_unicas,
                'views_totais': views_totais,
                'total_avaliacoes': total_avaliacoes,
                'proporcao_ruim': proporcao_ruim,
                'proporcao_bom': proporcao_bom,
                'proporcao_otimo': proporcao_otimo,
                'maior_avaliacao': maior_avaliacao,
            }
        )
