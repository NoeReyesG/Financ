from . import views
from django.urls import path

urlpatterns = [
   
    path("", views.index, name="home"),
    path("login", views.login_user, name = "login"),
    path("sign-in", views.signin,  name = "sign-in" ),
    path("logout", views.logout_view, name ="logout" ),
    path("registrar", views.registrarCliente, name="registrar"),
    path("consultar", views.consultar_cliente, name ="consultar"),
    path("cliente/<int:id>", views.cliente_config, name="cliente"),
    path("cliente/<int:id>/<str:mensaje>", views.cliente_config, name="cliente_mensaje"),

    #API
    path("pedidos", views.pedidos, name="pedidos"),
    path("nuevo-prestamo/<int:cliente_id>", views.nuevo_prestamo, name="nuevo-prestamo"),
    path("pago/<int:prestamo_id>", views.pago, name="pago"),
    path("update/<int:cliente_id>", views.update_cliente, name="update")

    #path('', views.home, name="home")

]