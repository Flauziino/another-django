from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.urls import reverse
from django.views import View


class CadastroView(View):
    def get(self, request):
        return render(request, 'cadastro.html')

    def post(self, request):
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
            messages.add_message(
                request,
                constants.SUCCESS,
                f'Usuario criado {username} com sucesso'
            )
            return redirect(reverse('login'))

        except:  # noqa: E722
            messages.add_message(
                request, constants.ERROR, 'Erro interno do servidor'
            )
            return redirect(reverse('cadastro'))


class LogarView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
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


class LogoutView(View):
    def get(self, request):
        auth.logout(request)

        messages.add_message(
            request,
            constants.SUCCESS,
            'Usuario deslogado com sucesso, volte sempre!'
        )
        return redirect(reverse('login'))
