from django.urls import path
from . import views


urlpatterns = [
    path(
        'novo_flashcard/',
        views.NovoFlashcard.as_view(),
        name="novo_flashcard"
    ),
    path(
        'deletar_flashcard/<int:id>',
        views.DeletarFlashcard.as_view(),
        name="deletar_flashcard"
    ),
    path('iniciar_desafio/', views.iniciar_desafio, name='iniciar_desafio'),
    path('listar_desafio/', views.listar_desafio, name='listar_desafio'),
    path('desafio/<int:id>/', views.desafio, name='desafio'),
    path(
        'responder_flashcard/<int:id>/',
        views.responder_flashcard,
        name='responder_flashcard'
    ),
    path('relatorio/<int:id>/', views.relatorio, name='relatorio'),
]
