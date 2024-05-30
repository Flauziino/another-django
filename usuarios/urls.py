from django.urls import path
from . import views

urlpatterns = [
    path(
        'cadastro/',
        views.CadastroView.as_view(),
        name="cadastro"
    ),
    path(
        'logar/',
        views.LogarView.as_view(),
        name="login"
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name="logout"
    ),
]
