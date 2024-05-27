from .models import Categoria, Flashcard, FlashcardDesafio, Desafio

from django.views import View
from django.http import Http404
from django.contrib import messages

from django.db.models import Q, Count, Value
from django.contrib.messages import constants
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.functions import Coalesce
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(
    login_required(login_url='login', redirect_field_name='next'),
    name='dispatch'
)
class NovoFlashcard(View):
    def get(self, request):
        categoria = Categoria.objects.all()
        dificuldade = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.all()

        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        if categoria_filtrar:
            flashcards = flashcards.filter(
                categoria__id=categoria_filtrar
            )

        if dificuldade_filtrar:
            flashcards = flashcards.filter(
                dificuldade=dificuldade_filtrar
            )

        return render(
            request,
            'novo_flashcard.html',
            {
                'categoria': categoria,
                'dificuldade': dificuldade,
                'flashcards': flashcards
            })

    def post(self, request):
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(
                request,
                constants.ERROR,
                'Preencha os campos de pergunta e resposta',
            )
            return redirect('/flashcard/novo_flashcard')

        flashcard = Flashcard(
            user=request.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade,
        )

        flashcard.save()

        messages.add_message(
            request,
            constants.SUCCESS,
            'Flashcard criado com sucesso'
        )
        return redirect('/flashcard/novo_flashcard')


@method_decorator(
    login_required(login_url='login', redirect_field_name='next'),
    name='dispatch'
)
class DeletarFlashcard(View):
    def get(self, request, id):
        flashcard = get_object_or_404(Flashcard, id=id)

        if request.user.id != flashcard.user.id:
            messages.add_message(
                request,
                constants.ERROR,
                'Voce nao pode deletar esse flashcard!'
            )
            return redirect('/flashcard/novo_flashcard')

        flashcard.delete()
        messages.add_message(
            request,
            constants.SUCCESS,
            'Flashcard deletado com sucesso!'
        )

        return redirect('/flashcard/novo_flashcard')


def iniciar_desafio(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES

        return render(
            request,
            'iniciar_desafio.html',
            {
                'categorias': categorias,
                'dificuldades': dificuldades
            },
        )

    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')

        desafio = Desafio(
            user=request.user,
            titulo=titulo,
            quantidade_perguntas=qtd_perguntas,
            dificuldade=dificuldade,
        )

        desafio.save()
        desafio.categoria.add(*categorias)

        flashcards = (
            Flashcard.objects.filter(user=request.user)
            .filter(dificuldade=dificuldade)
            .filter(categoria_id__in=categorias)
            .order_by('?')
        )

        if flashcards.count() < int(qtd_perguntas):
            return redirect('/flashcard/iniciar_desafio/')

        flashcards = flashcards[: int(qtd_perguntas)]

        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(
                flashcard=f,
            )
            flashcard_desafio.save()
            desafio.flashcards.add(flashcard_desafio)

        desafio.save()
        return redirect('/flashcard/listar_desafio/')


def listar_desafio(request):
    if request.method == 'GET':
        desafios = Desafio.objects.filter(user=request.user)
        status = FlashcardDesafio.objects.all()
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES

        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        if categoria_filtrar:
            desafios = desafios.filter(
                categoria__id=categoria_filtrar
            )

        if dificuldade_filtrar:
            desafios = desafios.filter(
                dificuldade=dificuldade_filtrar
            )

        # talvez esse status vai precisar de um loop
        return render(
            request,
            'listar_desafio.html',
            {
                'desafios': desafios,
                'status': status,
                'categorias': categorias,
                'dificuldades': dificuldades,
            },
        )


def desafio(request, id):
    desafio = Desafio.objects.get(id=id)

    if not desafio.user == request.user:
        raise Http404()

    if request.method == 'GET':
        acertos = (
            desafio.flashcards.filter(respondido=True)
            .filter(acertou=True)
            .count()
        )
        erros = (
            desafio.flashcards.filter(respondido=True)
            .filter(acertou=False)
            .count()
        )

        faltantes = (
            desafio.flashcards.filter(respondido=False)
            .count()
        )

        return render(
            request,
            'desafio.html',
            {
                'desafio': desafio,
                'acertos': acertos,
                'erros': erros,
                'faltantes': faltantes
            },
        )


def responder_flashcard(request, id):
    flashcard_desafio = FlashcardDesafio.objects.get(id=id)

    acertou = request.GET.get('acertou')
    desafio_id = request.GET.get('desafio_id')

    if not flashcard_desafio.flashcard.user == request.user:
        raise Http404()

    flashcard_desafio.respondido = True
    flashcard_desafio.acertou = True if acertou == '1' else False
    flashcard_desafio.save()

    return redirect(
        f'/flashcard/desafio/{desafio_id}/'
    )


def relatorio(request, id):
    desafio = Desafio.objects.get(id=id)

    acertos = desafio.flashcards.filter(acertou=True).count()
    erros = desafio.flashcards.filter(acertou=False).count()

    dados = [acertos, erros]

    categorias = desafio.categoria.all()

    melhores = []
    piores = []

    categorias_com_dados = categorias.annotate(
        total_flashcards=Count('flashcard'),
        acertos=Coalesce(Count('flashcard__flashcarddesafio', filter=Q(
            flashcard__flashcarddesafio__acertou=True)), Value(0)),
        erros=Coalesce(Count('flashcard__flashcarddesafio', filter=Q(
            flashcard__flashcarddesafio__acertou=False)), Value(0))
    )

    for categoria in categorias_com_dados:
        total_flashcards = categoria.total_flashcards

        if total_flashcards > 0:  # Para evitar divisão por zero
            proporcao_acertos = categoria.acertos / total_flashcards

            if proporcao_acertos >= 0.5:
                melhores.append(
                    {
                        'nome': categoria.nome,
                        'proporcao_acertos': proporcao_acertos,
                        'acertos': categoria.acertos,
                        'erros': categoria.erros
                    }
                )
            else:
                piores.append(
                    {
                        'nome': categoria.nome,
                        'proporcao_acertos': proporcao_acertos,
                        'acertos': categoria.acertos,
                        'erros': categoria.erros
                    }
                )

    # Preencher a lista de melhores com elementos vazios
    # para manter o html exibindo sempre os 3 melhores
    melhores.extend(
        [{
            'nome': 'N/A',
            'proporcao_acertos': 0,
            'acertos': 0,
            'erros': 0
        }] * (3 - len(melhores))
    )

    # Preencher a lista de piores com elementos vazios
    # para manter o html exibindo sempre os 3 piores
    piores.extend(
        [{
            'nome': 'N/A',
            'proporcao_acertos': 0,
            'acertos': 0,
            'erros': 0
        }] * (3 - len(piores))
    )

    # Classificar listas com base na proporção de acertos
    melhores = sorted(
        melhores, key=lambda x: x['proporcao_acertos'], reverse=True
    )[:3]
    piores = sorted(
        piores, key=lambda x: x['proporcao_acertos']
    )[:3]

    nome_categoria = [i.nome for i in categorias]

    nome_categoria = []
    for i in categorias:
        nome_categoria.append(i.nome)

    dados2 = []
    for categoria in categorias:
        dados2.append(
            desafio.flashcards.filter(flashcard__categoria=categoria)
            .filter(acertou=True)
            .count()
        )

    return render(
        request,
        'relatorio.html',
        {
            'desafio': desafio,
            'dados': dados,
            'categorias': nome_categoria,
            'dados2': dados2,
            'melhores': melhores,
            'piores': piores,
            # 'acerto_categoria': acertos_categoria,
            # 'erros_categoria': erros_categoria
        },
    )
