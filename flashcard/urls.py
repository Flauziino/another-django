from django.urls import path
from . import views


urlpatterns = [
    path(
        'novo_flashcard/',
        views.NovoFlashcardView.as_view(),
        name="novo_flashcard"
    ),
    path(
        'deletar_flashcard/<int:id>',
        views.DeletarFlashcardView.as_view(),
        name="deletar_flashcard"
    ),
    path(
        'iniciar_desafio/',
        views.IniciarDesafioView.as_view(),
        name='iniciar_desafio'
    ),
    path(
        'listar_desafio/',
        views.ListarDesafioView.as_view(),
        name='listar_desafio'
    ),
    path(
        'desafio/<int:id>/',
        views.DesafioView.as_view(),
        name='desafio'
    ),
    path(
        'responder_flashcard/<int:id>/',
        views.ResponderFlashcardView.as_view(),
        name='responder_flashcard'
    ),
    path(
        'relatorio/<int:id>/',
        views.RelatorioView.as_view(),
        name='relatorio'
    ),
]
