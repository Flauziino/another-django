from django.urls import path
from . import views


urlpatterns = [
    path(
        'adicionar_apostilas/',
        views.AdicionarApostilasView.as_view(),
        name='adicionar_apostilas'
    ),
    path(
        'apostila/<int:id>',
        views.ApostilaView.as_view(),
        name='apostila'
    ),
]
