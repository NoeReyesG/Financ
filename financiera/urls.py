from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.login_user, name = "login"),
    path("sign-in", views.signin,  name = "sign-in" ),
    path("logout", views.logout_view, name ="logout" ),
    path("registrar", views.registrarCliente, name="registrar"),
    path("consultar", views.consultar_cliente, name ="consultar"),
    path("cliente/<int:id>", views.cliente_config, name="cliente")

    #path('', views.home, name="home")

]