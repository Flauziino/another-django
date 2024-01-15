from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth


def cadastro(request):
    if request.method == 'GET':
        return render(
            request,
            'cadastro.html'
        )

    elif request.method == 'POST':
        # pegando um dado por vez do form
        # dentro do get usa o nome que foi dado ao input
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not username:
            return redirect('/usuarios/cadastro')

        if not senha:
            return redirect('/usuarios/cadastro')

        if not senha == confirmar_senha:
            messages.add_message(
                request, constants.ERROR, 'As senhas nao coincidem'
            )
            return redirect('/usuarios/cadastro')

        # verificando se o usuario existe no BD
        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(
                request, constants.ERROR, 'Esse nome de usuario ja existe'
            )
            return redirect('/usuarios/cadastro')

        try:
            User.objects.create_user(
                username=username,
                password=senha
            )
            return redirect(reverse('login'))

        except:
            messages.add_message(
                request, constants.ERROR, 'Erro interno do servidor'
            )
            return redirect('usuarios/cadastro')


def logar(request):
    if request.method == 'GET':
        return render(
            request,
            'login.html'
            )

    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(
            request,
            username=username,
            password=senha
        )

        if user:
            auth.login(
                request,
                user
            )
            messages.add_message(
                request,
                constants.SUCCESS, 'Usuario logado com sucesso!'
            )
            return redirect('/flashcard/novo_flashcard/')

        else:
            messages.add_message(
                request,
                constants.ERROR,
                'Username ou senha invalidos'
            )

            return redirect(reverse('login'))


def logout(request):
    auth.logout(request)

    messages.add_message(
        request,
        constants.SUCCESS,
        'Usuario deslogado com sucesso, volte sempre!'
    )
    return redirect(reverse('login'))
