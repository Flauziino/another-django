from django.shortcuts import render, redirect
from .models import Apostila, ViewApostila
from django.contrib.messages import constants
from django.contrib import messages


def adicionar_apostilas(request):
    apostilas = Apostila.objects.filter(user=request.user)
    apostila_tag = None
    views_totais = (
        ViewApostila.objects.filter(apostila__user=request.user)
        .count()
        )
    if request.method == 'GET':

        return render(
            request,
            'adicionar_apostilas.html',
            {
                'apostilas': apostilas,
                'views_totais': views_totais
            }
        )

    elif request.method == 'POST':
        busca = request.POST.get('tags', '')
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

        return render(
            request,
            'adicionar_apostilas.html',
            {
                'apostilas': apostilas,
                'views_totais': views_totais,
                'apostila_tag': apostila_tag
            }
        )


def apostila(request, id):
    apostila = Apostila.objects.get(id=id)

    if request.method == "GET":
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
            }
        )
